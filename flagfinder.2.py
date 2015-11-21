#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

String cascade_name = "cascade.xml";
CascadeClassifier cascade;

int main( int argc, const char** argv )
{
    if(argc > 2)
    {
        printf("Please provide an input image.\n");
        return 0;
    }

    if( !cascade.load(cascade_name))
    {
        printf("--(!)Error loading cascade.xml\n");
        return 9;
    }

    Mat img = imread(argv[1], CV_LOAD_IMAGE_COLOR);

    Size size(1024,768);
    Mat image;
    resize(img, image, size);
    std::vector<Rect> faces;
    Mat frame_gray;

    cvtColor(image, frame_gray, CV_BGR2GRAY );
    equalizeHist( frame_gray, frame_gray );

    //-- Detect faces
    cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(60, 60) );

    cout << "found: " << faces.size() << endl;

    if(faces.size())
        return 1;

    return 0;
}

