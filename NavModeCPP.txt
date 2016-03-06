#include<iostream>
#include<string>
#include<conio.h>
#include<algorithm>
#include<vector>
#include<opencv/highgui.h>
#include<opencv2/opencv.hpp>
#include<opencv2/imgproc.hpp>
#include<Windows.h>
#include<Winuser.h>
#include<list>

using namespace std;

int H_MIN = 0;
int H_MAX = 256;
int S_MIN = 0;
int S_MAX = 256;
int V_MIN = 0;
int V_MAX = 256;

const int FRAME_WIDTH = 1366;	// Window Size
const int FRAME_HEIGHT = 768;

bool caliberationMode = true, mouseisDragging, mouseMove, rectangleSelected;

cv::Point initialClickPoint, currentMousePoint;
cv::Rect rectangleROI;

vector<int> H_ROI, S_ROI, V_ROI;

const string original_window = "Original Image";
const string hsv_image_window = "HSV Image";
const string threshold_image_window = "Thresholded Image";
const string morphed_image_window = "After morphological operations";



void applyMorphs(cv::Mat& thresh){

	cv::Mat erodeElement = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(3, 3));
	cv::Mat dialateElement = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(4, 4));

	cv::erode(thresh, thresh, erodeElement);
	cv::erode(thresh, thresh, erodeElement);

	cv::dilate(thresh, thresh, dialateElement);
	cv::dilate(thresh, thresh, dialateElement);
}


int main(int argc, char* argv[]){
	FreeConsole();
	cv::Mat camerafeed, camerafeedraw, HSV, threshold, captured_image;
	cv::VideoCapture capture;
	try{
		capture.open(0);
	}
	catch (exception e){
		return -1;
	}

	if (!capture.isOpened()){
		return -1;
	}

	capture.set(CV_CAP_PROP_FRAME_WIDTH, FRAME_WIDTH);
	capture.set(CV_CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT);
//	cv::namedWindow(original_window);
	int pposX = 0, pposY = 0;

	list<cv::Point> lastfivevals(2, cv::Point(0, 0));

	int errorcode = 0;

	while (1){
		try{
			capture.read(camerafeedraw);
			cv::flip(camerafeedraw, camerafeed, 1);
			//cv::blur(captured_image, camerafeed, cv::Size(3, 3), cv::Point(-1, -1));
			cv::cvtColor(camerafeed, HSV, CV_BGR2HSV);	// Convert BGR to HSV

			cv::Mat lower_red_hue_range;
			cv::Mat upper_red_hue_range;
			cv::inRange(HSV, cv::Scalar(0, 100, 100), cv::Scalar(10, 255, 255), lower_red_hue_range);
			cv::inRange(HSV, cv::Scalar(160, 100, 100), cv::Scalar(179, 255, 255), upper_red_hue_range);

			cv::Mat red_hue_image;
			cv::addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0, red_hue_image);	// Combine both lower and upper half
			applyMorphs(red_hue_image);
			applyMorphs(red_hue_image);
			applyMorphs(red_hue_image);
			cv::GaussianBlur(red_hue_image, red_hue_image, cv::Size(9, 9), 2, 2);

			vector<vector<cv::Point>> contours;

			findContours(red_hue_image, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);

			int largest_area = 0, largest_contour_index = -1;

			for (int i = 0; i < contours.size(); i++) // iterate through each contour. 
			{
				double a = contourArea(contours[i], false);  //  Find the area of contour
				if (a > largest_area){
					largest_area = a;
					largest_contour_index = i;                //Store the index of largest contour
				}

			}
			if (largest_contour_index == -1)
				continue;

			cv::Moments objMoment = cv::moments(contours[largest_contour_index]);		// Find Moments

			double dM01 = objMoment.m01;
			double dM10 = objMoment.m10;
			double dArea = objMoment.m00;

			int posX = dM10 / dArea;		// Find X and Y coordinates of the Blob/Obj
			int posY = dM01 / dArea;
			lastfivevals.pop_front();
			lastfivevals.push_back(cv::Point(posX, posY));
			cv::Point avg(0, 0);
			for (cv::Point p : lastfivevals){	// Taking avg. of last 5 points
				avg.x += p.x;
				avg.y += p.y;
			}
			posX = avg.x / 2;
			posY = avg.y / 2;

			if (abs(posX) <= FRAME_WIDTH && abs(posY) <= FRAME_HEIGHT){
				try{
					//SetCursorPos(-pposX+posX+FRAME_WIDTH/2,-pposY+posY+FRAME_HEIGHT/2);
					SetCursorPos(posX, posY);
					pposX = posX;
					pposY = posY;
					cv::circle(camerafeed, cv::Point(posX, posY), 100, cv::Scalar(255, 0, 0), 10, 8);
				}
				catch (exception e){
					continue;
				}
			}
			/*
			cv::imshow(original_window, camerafeed);
			cv::imshow(hsv_image_window, HSV);
			cv::imshow(threshold_image_window, red_hue_image);
			*/
		}
		catch (exception e){
			errorcode++;
			if (errorcode > 3)
				break;
			else
				continue;
		}

		if (cv::waitKey(30) == 'c')
			caliberationMode = !caliberationMode;

	}
	return 0;
}
