slowloris-dos
=============

This experimental node.js application is a experiment to see if node.js can be used for denial of service attacks. This specific implementation creates slowloris attack.

## Installation

### 1. Install dependencies
Download and install [node.js](http://nodejs.org/download/)

### 2. Open the directory of this file in command line
In the command line interface, type:

```bash
cd /path/to/slowloris-dos/
```

### 3. Install project-specific dependencies
In the command line interface type:

```bash
npm install
```

### 4. Execute

```bash
node index.js [target] [socks address]
node index.js http://example.com localhost:9051
```
