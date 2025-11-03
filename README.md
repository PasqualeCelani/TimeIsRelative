# TimeIsRelative
A challenge for the 2025-2026 Computer Vision course at Sapienza University of Rome has been proposed which is **<ins>determining the time from a given image of an analog clock</ins>**. To make this challenge more interesting the proposal suggests that the use of all deep learning techniques, including Neural Networks and CNNs, be strictly prohibited. For an added twist, I propose a solution relying solely on traditional computer vision methods. Ready to see it in action? Keep reading bellow.

![alt text](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fuploads5.wikiart.org%2Fimages%2Fsalvador-dali%2Fthe-persistence-of-memory-1931.jpg&f=1&nofb=1&ipt=54772cea3d297a32066d522916e61dfdfbe8b78bcf9327d151a6bb036b4f3c39)

## Quick start

### Requirements
Ensure you have Python 3.12 (any modern version should be also ok) installed.

### Execution steps
1. Clone the repository:  `git clone https://github.com/PasqualeCelani/TimeIsRelative.git`
2. Go to the application directory: `cd TimeIsRelative`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment (Unix): `source ./venv/bin/activate`
5. Install the dependecies of the output project: `pip install -r requirements.txt
6. Run the application: `python main.py`

### Output
A successful run will result in a new window opening, showing an image identical to the one you see below.

![alt text](https://github.com/PasqualeCelani/TimeIsRelative/blob/main/data/output_img4.png)

In the terminal instead your output must look like: "The time is: 10:9 :)". If this is you case well done!

## Methodology
The used methodology relies entirely on exploiting the invariant features of an analog clock face. Specifically, is leverage the fact that the clock face is always a circle and that both the hour and minute hands always originate from its central point (plus some error due to issues with the clock circle recognition). 

The process follows the following steps:
1. **Circle Detection:** The algorithm first detects the circular boundary of the clock face using HoughCircles method. If no  circular boundary or more than one are found then an exception is raised since this is a mandatory step to detect the clock;
2. **Hand Detection:** Once the main circular boundary is found the main image is masked to keep just the conten inside the circle. To minimize distraction from irrelevant background elements I apply a mask to the image, focusing processing only on the pixels within the circular clock boundary. The process continues with the Canny edge detector which is mandatory before I employ HoughLinesP to find potential line segments within the clock face. If lines are found, they must be near the center of the circle as stated before, but what does mean near here? The spatial proximity is defined by a threshold which I set to 15% of the circle's radius. Every line segment that satisfies this rule is retained along with its length. If the filter yields fewer than two candidate lines, it is trivial to say these are not the clock hands, so I raise an exception. Finally, assuming at least two valid lines are detected, we sort them by length to establish their identity. As usual the shortest  line segment is designated as the hour hand, and the longest is designated as the minute hand;
3. **Orientation Calculation:** Once i have the two line segments of the minutes and hours it's time to calculate the precise angular orientation of each one, one for the hour and one for the minute relative to the circle's top. In dettail, the arctan2 is used to calculate the angle. The $atan2(y, x)$ returns the angle $\theta$ between the positive x-axis and the ray from the origin to the point $(x, y)$, confined to $(-\pi, \pi]$. For example we can see the image bellow.<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Atan2_differs_from_arctan.png/250px-Atan2_differs_from_arctan.png" alt="Atan2 differs from arctan" width="400"/></p> Practically the required vector for $atan2$ is calculated as $x=\Delta_x$ = $Center_x$ - $TopLine_x$ and $y=\Delta_y$ = $Center_y$ - $TopLine_y$. $atan2(y, x)$ return the angle in radians, I convert it to degree since for me are more interpretable. In dettail, I want them between 0% abd 360% to archive this i sum the result with 360 and I take the module of 360;
4. **Time Approximation:**  
