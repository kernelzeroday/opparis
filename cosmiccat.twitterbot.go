package main
/**
	Twitter Accounts, Links and Hashtags Searcher
	v 0.2
	by CosmicCat
	cosmiccat@i2pmail.org
 */
import (
	"net/http"
	"os"
	"fmt"
	"net/url"
	"io/ioutil"
	"io"
	"bytes"
	"gopkg.in/xmlpath.v2"
	"strings"
	"golang.org/x/net/html"
	"encoding/json"
	"runtime/debug"
	"runtime"
	"bufio"
	"math/rand"
)

var (
	domain = "https://twitter.com/"
	configFile = "./config.json"
	detailedDir = "detailed"
	accountDir = "by_accounts"
	hashtagDir = "by_hashtags"
	resultsDir = "results"
	sortedDir = "sorted"
	unsortedDir = "unsorted"
	hashtagsFile = "hashtags.txt"
	externalLinksFile = "external_links.txt"
	userAccountsFile = "accounts.txt"
	config Config
	hashtagsToSearch map[string]struct{}
	accountsToSearch map[string]struct{}
	findedAccountsToSearch map[string]struct{}
	hashtagsByAccount map[string]map[string]struct{}
	totalHashtags map[string]struct{}
	externalLinksByAccount map[string]map[string]struct{}
	totalExternalLinks map[string]struct{}
	userAccountsByAccount map[string]map[string]struct{}
	totalUserAccounts map[string]struct{}
	hashtagsByHashtag map[string]map[string]struct{}
	userAccountsByHashtag map[string]map[string]struct{}
	externalLinksByHashtag map[string]map[string]struct{}
)

type Config struct {
	DetailedData    bool
	ProxyHost       string
	ProxyPort       string
	HashtagsFile    string
	AccountsFile    string
	Shuffle         bool
	RecursiveSearch bool
	Threads         int
	UseThreads      bool
}

func main() {
	prepares()
	if config.UseThreads {
		goSearchHashtags()
		goSearchAccounts(accountsToSearch)
		goSearchAccounts(findedAccountsToSearch)
	} else {
		for _, hashtag := range (getShuffledValues(hashtagsToSearch)) {
			loadHashtag(hashtag)
		}
		for _, account := range (getShuffledValues(accountsToSearch)) {
			loadAccount(account)
		}
		if config.RecursiveSearch {
			for account, _ := range (findedAccountsToSearch) {
				loadAccount(account)
			}
		}
	}
	saveTotal()
	fmt.Println("Finished!")
}

func goSearchHashtags() {
	sem := make(chan bool, config.Threads)
	for hashtag, _ := range (hashtagsToSearch) {
		sem <- true
		go func(ht string) {
			defer func() {
				<-sem
				runtime.GC()
				debug.FreeOSMemory()
			}()
			loadHashtag(ht)
		}(hashtag)
	}
	for i := 0; i < cap(sem); i++ {
		sem <- true
	}
}

func goSearchAccounts(accounts map[string]struct{}) {
	fmt.Println("start search accounts")
	sem := make(chan bool, config.Threads)
	for account, _ := range (accounts) {
		sem <- true
		go func(acc string) {
			defer func() {
				<-sem
				runtime.GC()
				debug.FreeOSMemory()
			}()
			loadAccount(acc)
		}(account)
	}
	for i := 0; i < cap(sem); i++ {
		sem <- true
	}
}

func loadHashtags() {
	if config.HashtagsFile != "" {
		if _, err := os.Stat(config.HashtagsFile); !os.IsNotExist(err) {
			inFile, _ := os.Open(config.HashtagsFile)
			defer inFile.Close()
			scanner := bufio.NewScanner(inFile)
			scanner.Split(bufio.ScanLines)
			for scanner.Scan() {
				hashtagsToSearch[strings.Replace(scanner.Text(), "#", "", -1)] = struct{}{}
			}
		}
	}
}

func loadAccounts() {
	if config.AccountsFile != "" {
		if _, err := os.Stat(config.AccountsFile); !os.IsNotExist(err) {
			inFile, _ := os.Open(config.AccountsFile)
			defer inFile.Close()
			scanner := bufio.NewScanner(inFile)
			scanner.Split(bufio.ScanLines)
			for scanner.Scan() {
				accountsToSearch[strings.Replace(strings.Replace(scanner.Text(), "@", "", -1), domain, "", -1)] = struct{}{}
			}
		}
	}
}

func saveTotal() {
	fullSortedDir := resultsDir + "/" + sortedDir + "/"
	for hashtag := range (totalHashtags) {
		writeToFile(fullSortedDir + hashtagsFile, "#" + hashtag)
	}
	totalHashtags = make(map[string]struct{})
	for extLink := range (totalExternalLinks) {
		writeToFile(fullSortedDir + externalLinksFile, extLink)
	}
	totalExternalLinks = make(map[string]struct{})
	for account := range (totalUserAccounts) {
		writeToFile(fullSortedDir + userAccountsFile, "@" + account)
	}
	totalUserAccounts = make(map[string]struct{})
	runtime.GC()
	debug.FreeOSMemory()
}

func prepares() {
	checkConfig()
	proxyUrl, _ := url.Parse("http://" + config.ProxyHost + ":" + config.ProxyPort)
	http.DefaultTransport = &http.Transport{Proxy: http.ProxyURL(proxyUrl)}
	checkAndMakeDir(resultsDir)
	if config.DetailedData {
		checkAndMakeDir(resultsDir + "/" + detailedDir)
		checkAndMakeDir(resultsDir + "/" + detailedDir + "/" + accountDir)
		checkAndMakeDir(resultsDir + "/" + detailedDir + "/" + hashtagDir)
	}
	checkAndMakeDir(resultsDir + "/" + sortedDir)
	checkAndMakeDir(resultsDir + "/" + unsortedDir)
	hashtagsByAccount = make(map[string]map[string]struct{})
	totalHashtags = make(map[string]struct{})
	externalLinksByAccount = make(map[string]map[string]struct{})
	totalExternalLinks = make(map[string]struct{})
	userAccountsByAccount = make(map[string]map[string]struct{})
	totalUserAccounts = make(map[string]struct{})
	accountsToSearch = make(map[string]struct{})
	hashtagsToSearch = make(map[string]struct{})
	findedAccountsToSearch = make(map[string]struct{})
	userAccountsByHashtag = make(map[string]map[string]struct{})
	externalLinksByHashtag = make(map[string]map[string]struct{})
	hashtagsByHashtag = make(map[string]map[string]struct{})
	loadHashtags()
	loadAccounts()
}

func getShuffledValues(src map[string]struct{}) (dest []string) {
	keys := make([]string, 0, len(src))
	for k := range src {
		keys = append(keys, k)
	}
	if config.Shuffle {
		dest = make([]string, len(keys))
		perm := rand.Perm(len(keys))
		for i, v := range perm {
			dest[v] = keys[i]
		}
	} else {
		dest = keys
	}
	return
}

func checkConfig() {
	if _, err := os.Stat(configFile); os.IsNotExist(err) {
		default_conf := &Config{
			UseThreads: false,
			Threads: 4,
			RecursiveSearch: true,
			Shuffle: true,
			HashtagsFile: "./tags.txt",
			AccountsFile: "./targets.txt",
			ProxyHost: "127.0.0.1",
			ProxyPort: "8118",
			DetailedData: true}
		jsonStr, _ := json.Marshal(default_conf)
		out, _ := os.Create(configFile)
		io.Copy(out, bytes.NewReader(jsonStr))
		log("Default config saved. Check and change config file \"" + configFile + "\"!")
		os.Exit(0)
	}
	file, _ := ioutil.ReadFile(configFile)
	config = Config{}
	json.Unmarshal(file, &config)
	log("Config loaded")
}

func loadHashtag(hashtag string) {
	rootNode := getRootNode(domain + "search?q=" + url.QueryEscape("#" + hashtag))
	if rootNode == nil {
		log("Root node is absend for #" + hashtag)
		return
	}
	hashtagsByHashtag[hashtag] = make(map[string]struct{})
	externalLinksByHashtag[hashtag] = make(map[string]struct{})
	userAccountsByHashtag[hashtag] = make(map[string]struct{})
	handleTweets(rootNode, hashtag, false)
	min_position_path := xmlpath.MustCompile("//div[@id='timeline']//div[contains(@class,'stream-container')]/@data-min-position")
	min_position, ok := min_position_path.String(rootNode)
	if !ok {
		log("Skipping page of #" + hashtag)
	} else {
		loadTweetsByHashtag(min_position, hashtag)
		fullDir := resultsDir + "/" + detailedDir + "/" + hashtagDir + "/" + hashtag
		if config.DetailedData {
			checkAndMakeDir(fullDir)
			for hashtag := range (hashtagsByHashtag[hashtag]) {
				writeToFile(fullDir + "/" + hashtagsFile, "#" + hashtag)
			}
			for externalLink := range (externalLinksByHashtag[hashtag]) {
				writeToFile(fullDir + "/" + externalLinksFile, externalLink)
			}
		}
		for userAccount := range (userAccountsByHashtag[hashtag]) {
			if config.DetailedData {
				writeToFile(fullDir + "/" + userAccountsFile, "@" + userAccount)
			}
			if config.RecursiveSearch {
				if _, ok := accountsToSearch[userAccount]; !ok {
					findedAccountsToSearch[userAccount] = struct{}{};
				}
			}
		}
	}
	delete(hashtagsByHashtag, hashtag)
	delete(externalLinksByHashtag, hashtag)
	delete(userAccountsByHashtag, hashtag)
	runtime.GC()
	debug.FreeOSMemory()
}

func loadAccount(account string) {
	log("Start search account " + domain + account)
	rootNode := getRootNode(domain + account)
	if rootNode == nil {
		log("Root node is absend for @" + account)
		return
	}
	hashtagsByAccount[account] = make(map[string]struct{})
	externalLinksByAccount[account] = make(map[string]struct{})
	userAccountsByAccount[account] = make(map[string]struct{})
	handleTweets(rootNode, account, true)
	min_position_path := xmlpath.MustCompile("//div[@id='timeline']//div[contains(@class,'stream-container')]/@data-min-position")
	min_position, ok := min_position_path.String(rootNode)
	if !ok {
		log("Skipping page of @" + account)
	} else {
		loadTweets(min_position, account)
		fullDir := resultsDir + "/" + detailedDir + "/" + accountDir + "/" + account
		if config.DetailedData {
			checkAndMakeDir(fullDir)
			for hashtag := range (hashtagsByAccount[account]) {
				writeToFile(fullDir + "/" + hashtagsFile, "#" + hashtag)
			}
			for externalLink := range (externalLinksByAccount[account]) {
				writeToFile(fullDir + "/" + externalLinksFile, externalLink)
			}
		}
		for userAccount := range (userAccountsByAccount[account]) {
			if config.DetailedData {
				writeToFile(fullDir + "/" + userAccountsFile, "@" + userAccount)
			}
			if config.RecursiveSearch {
				if _, ok := accountsToSearch[userAccount]; !ok {
					findedAccountsToSearch[userAccount] = struct{}{};
				}
			}
		}
	}
	delete(hashtagsByAccount, account)
	delete(externalLinksByAccount, account)
	delete(userAccountsByAccount, account)
	runtime.GC()
	debug.FreeOSMemory()
}

func loadTweetsByHashtag(max_tweet string, hashtag string) {
	urlToLoad := "https://twitter.com/i/search/timeline?vertical=default&q=%23" + hashtag + "&src=typd&include_available_features=1&include_entities=1&last_note_ts=7456&max_position=" + max_tweet
	req, err := http.NewRequest("GET", urlToLoad, nil)
	if err != nil {
		log("Error1: " + err.Error())
	} else {
		response, err := http.DefaultTransport.RoundTrip(req)
		if err != nil {
			log("Error2: " + err.Error())
		} else {
			defer response.Body.Close()
			content, err := ioutil.ReadAll(response.Body)
			if err != nil {
				log("Error3: " + err.Error())
			} else {
				var data interface{}
				if err := json.Unmarshal(content, &data); err != nil {
					log("Error4: " + err.Error())
				}
				m := data.(map[string]interface{})
				innerHtml := m["items_html"]
				has_more_i := m["has_more_items"]
				min_position_i := m["min_position"]
				str, _ := innerHtml.(string)
				has_more, _ := has_more_i.(bool)
				min_position, _ := min_position_i.(string)
				root, err := html.Parse(bytes.NewReader([]byte(str)))
				if err != nil {
					log("Error5: " + err.Error())
				}
				var b bytes.Buffer
				html.Render(&b, root)
				fixedHtml := b.String()
				reader := strings.NewReader(fixedHtml)
				rootNode, err := xmlpath.ParseHTML(reader)
				if err != nil {
					log("Error6: " + err.Error())
				} else {
					handleTweets(rootNode, hashtag, false)
					if has_more == true {
						loadTweetsByHashtag(min_position, hashtag)
					}
				}
			}
		}
	}
}

func loadTweets(max_position string, account string) {
	log("Loading tweets for @" + account + "... [" + max_position + "]")
	urlToLoad := "https://twitter.com/i/profiles/show/" + account + "/timeline?include_available_features=1&include_entities=1&reset_error_state=false&max_position=" + max_position
	req, err := http.NewRequest("GET", urlToLoad, nil)
	if err != nil {
		log("Error1: " + err.Error())
	} else {
		response, err := http.DefaultTransport.RoundTrip(req)
		if err != nil {
			log("Error2: " + err.Error())
		} else {
			defer response.Body.Close()
			content, err := ioutil.ReadAll(response.Body)
			if err != nil {
				log("Error3: " + err.Error())
			} else {
				var data interface{}
				if err := json.Unmarshal(content, &data); err != nil {
					log("Error4: " + err.Error())
				}
				m := data.(map[string]interface{})
				innerHtml := m["items_html"]
				has_more_i := m["has_more_items"]
				min_position_i := m["min_position"]
				str, _ := innerHtml.(string)
				has_more, _ := has_more_i.(bool)
				min_position, _ := min_position_i.(string)
				root, err := html.Parse(bytes.NewReader([]byte(str)))
				if err != nil {
					log("Error5: " + err.Error())
				}
				var b bytes.Buffer
				html.Render(&b, root)
				fixedHtml := b.String()
				reader := strings.NewReader(fixedHtml)
				rootNode, err := xmlpath.ParseHTML(reader)
				if err != nil {
					log("Error6: " + err.Error())
				} else {
					handleTweets(rootNode, account, true)
					if has_more == true && min_position != "" {
						loadTweets(min_position, account)
					}
				}
			}
		}
	}
}

func handleTweets(rootNode *xmlpath.Node, what string, is_account bool) {
	handleHashtags(rootNode, what, is_account)
	handleExternalLinks(rootNode, what, is_account)
	handleAccounts(rootNode, what, is_account)
}

func handleAccounts(rootNode *xmlpath.Node, what string, is_account bool) {
	accountsNodes := xmlpath.MustCompile("//div[contains(@class,'stream-container')]//span[contains(@class,'username')]//b")
	iter := accountsNodes.Iter(rootNode)
	for iter.Next() {
		accountLink := iter.Node().String()
		if config.DetailedData {
			if is_account {
				userAccountsByAccount[what][accountLink] = struct{}{}
			} else {
				userAccountsByHashtag[what][accountLink] = struct{}{}
			}
		}
		totalUserAccounts[accountLink] = struct{}{}
		writeToFile(resultsDir + "/" + unsortedDir + "/" + userAccountsFile, "@" + accountLink)
	}
}

func handleExternalLinks(rootNode *xmlpath.Node, what string, is_account bool) {
	linksNodes := xmlpath.MustCompile("//div[contains(@class,'stream-container')]//a[contains(@class,'twitter-timeline-link')]/@data-expanded-url")
	iter := linksNodes.Iter(rootNode)
	for iter.Next() {
		externalLink := iter.Node().String()
		if config.DetailedData {
			if is_account {
				externalLinksByAccount[what][externalLink] = struct{}{}
			} else {
				externalLinksByHashtag[what][externalLink] = struct{}{}
			}
		}
		totalExternalLinks[externalLink] = struct{}{}
		writeToFile(resultsDir + "/" + unsortedDir + "/" + externalLinksFile, externalLink)
	}
}

func handleHashtags(rootNode *xmlpath.Node, what string, is_account bool) {
	hashtagsNodes := xmlpath.MustCompile("//a[contains(@class,'twitter-hashtag')]//b")
	iter := hashtagsNodes.Iter(rootNode)
	for iter.Next() {
		hashtag := iter.Node().String()
		if config.DetailedData {
			if is_account {
				hashtagsByAccount[what][hashtag] = struct{}{}
			} else {
				hashtagsByHashtag[what][hashtag] = struct{}{}
			}
		}
		totalHashtags[hashtag] = struct{}{}
		writeToFile(resultsDir + "/" + unsortedDir + "/" + hashtagsFile, "#" + hashtag)
	}
}

func checkAndMakeDir(dir string) {
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		os.Mkdir(dir, 0600)
	}
}

func getRootNode(urlToOpen string) (*xmlpath.Node) {
	req, err := http.NewRequest("GET", urlToOpen, nil)
	if (err != nil) {
		log("error1: " + err.Error())
	} else {
		response, err := http.DefaultTransport.RoundTrip(req)
		if (err != nil) {
			log("Error 3: " + err.Error())
		} else {
			defer response.Body.Close()
			content, err := ioutil.ReadAll(response.Body)
			if err != nil {
				log("Error 2: " + err.Error())
			} else {
				root, err := html.Parse(bytes.NewReader(content))

				if err != nil {
					log("Parse error: " + err.Error())
				}

				var b bytes.Buffer
				html.Render(&b, root)
				fixedHtml := b.String()
				reader := strings.NewReader(fixedHtml)
				rootNode, err := xmlpath.ParseHTML(reader)
				if err != nil {
					log("Error 4: " + err.Error())
				} else {
					return rootNode
				}
			}
		}
	}
	return nil
}

func log(text string) {
	f, err := os.OpenFile("log.txt", os.O_APPEND | os.O_WRONLY | os.O_CREATE, 0600)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	fmt.Println(text)
	text = text + "\r\n\r\n"
	if _, err = f.WriteString(text); err != nil {
		panic(err)
	}
}

func writeToFile(file string, text string) {
	f, err := os.OpenFile(file, os.O_APPEND | os.O_WRONLY | os.O_CREATE, 0600)
	if err != nil {
		log("Error 1 on write file \"" + file + "\"")
	}
	defer f.Close()
	text = text + "\r\n"
	if _, err = f.WriteString(text); err != nil {
		log("Error 2 on write file \"" + file + "\"")
	}
}