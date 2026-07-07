# **0. Getting Started**

When you first enter the interface, the system provides an onboarding screen for creating an account, as shown in Figure 1.
Follow the prompts and enter the administrator account name and password.

![][embedded-image-1]

**Figure 1**

# **1. Quick Start Guide**

0. Go to **Map > General** to configure the map and Home Point.
1. **Set the Home Point (origin)**  
   After entering the system, go to **Map > General** and click **Home Point** to set the robot dog's starting position.  
2. **Create an inspection route**  
   After setting the Home Point, go to **Map > Route** to create the required inspection route.  
3. **Create an inspection plan**  
   Next, go to **Map > Plan** and combine the created routes into an inspection plan.  
4. **Start inspection**  
   After completing the settings above, the robot dog will automatically start executing the inspection plan.



# **2. Home**

As shown in Figure 2, select **Home** from the sidebar to open the home page. You can also switch pages from the sidebar.

![][image2]

**Figure 2**

## Dashboard

As shown in Figure 3, you can perform non-scheduled real-time operations from the Dashboard. You can pause, resume, or clear the robot dog's current task here.  
You can also directly command the robot dog to go to or execute a predefined Goal, Route, or Patrol Plan, or command it to return Home.  
In addition, you can control the robot dog's headlight, switch operating modes, enable the microphone, and play preset sound effects.

| Icon | Description |
| :---- | :---- |
| ![][image3] | Displays upcoming inspection schedules. Click to view the robot dog's inspection plans for the next three days, and skip or resume the current inspection plan. |
| ![][image4] | Click to preview or download the latest inspection report, which includes all AI detection events from the inspection. |
| ![][image5] | Click to switch to Manual Mode. When the robot dog is idle, it can be controlled with the joystick. |
| ![][image6] | Displays the map currently used by the robot dog. Click to switch to and preview other maps. |
| ![][image7] | Clears the robot dog's current task. |
| ![][image8]/![][image9] | Pauses or resumes the robot dog's current task. |
| ![][image10] | Commands the robot dog to return Home. |
| ![][image11] | Click to select a destination on the map. After confirmation, the robot dog will move to that location. |
| ![][image12] | Click to select a predefined Route. After confirmation, the robot dog will execute it immediately. |
| ![][image13] | Click to select a predefined Goal. After confirmation, the robot dog will go there immediately. |
| ![][image14] | Click to open a dialog for selecting a preset inspection plan. In the dialog, you can preview the inspection route, choose whether to start from the nearest point or execute the full plan, and decide whether to return Home after completion. After confirmation, the robot dog will immediately execute the selected plan. |
| ![][image15] | Click to open the control panel, where you can enable the microphone, play preset sound effects, adjust the headlight, and switch behavior modes. |

![][image16]

**Figure 3**

## System Overview

As shown in Figure 4, this section provides an overview of system information.

### Recent Events

The Recent Events panel displays recent robot dog activities, including system errors, AI detection events, and emergency events. Click the upper-right corner to view more events.

### Task List

The Task List panel displays the latest task execution results. Click the upper-right corner to view more records and detailed information.

### Status

The Status panel displays the robot dog's current status, including battery level, charging status, maximum motor temperature, current speed, and emergency button status.

![][image17]

**Figure 4**

## Live Video

As shown in Figure 5, you can view live video from the main camera and the left and right side cameras in this section. You can also refresh or pause the video using the buttons in the upper-right corner.

![][image18]

**Figure 5**

# **3. Map Page**

## Home Position Settings

1. As shown in Figure 6, select **Map** from the sidebar to open the map settings page.  
2. As shown in Figure 7, select **General** from the top menu to open the general settings page.  
3. Click **Home Point** to open the settings dialog, as shown in Figure 8.  
4. Select a map from the lower-left corner.  
5. After the map is displayed, click the map to set the Home position.  
6. Adjust the orientation on the right so that it faces the charging dock.

![][image19]

**Figure 6**

![][image20]

**Figure 7**

![][image21]

**Figure 8**

## Initial Pose

If localization has drifted, click the **Initial Pose** button, as shown in Figure 6, and select the current position, as shown in the figure.

![][image-init-pose]

**Figure: Initial Pose**

## Goal Management

1. On the map settings page, as shown in Figure 9, select **Goal** from the top menu to open the Goal settings page.  
2. Click the **"+"** button in the upper-right corner to open the Goal settings dialog, as shown in Figure 10.  
3. Select a map, enter a name, and enter or select a group name.  
4. After the map is displayed, click the map to set the Goal position.  
5. Set the **Degree** below to define the direction the robot dog should face during inspection.
6. You can click a card to enter the editing page. On this page, you can edit or delete the Goal, as shown in the goal edit figure.

![][image22]

**Figure 9**

![][image23]

**Figure 10**

![][goal-edit]

**Figure: Goal Edit**



## Route Management

1. On the map settings page, as shown in Figure 11, select **Route** from the top menu to open the Route settings page.  
2. Click the **"+"** button in the upper-right corner to open the Route settings dialog, as shown in Figure 12.  
3. Select a map, enter a name, select the AI detection mode and event type, and set the speed level for the route.  
4. After the map is displayed, click multiple points on the map in sequence to define the route, then adjust **Degree** on the right to set the robot dog's orientation at each point.
5. You can click a card to enter the editing page. On this page, you can edit or delete the Route, as shown in the route edit figure.

![][image24]

**Figure 11**

![][image25]

**Figure 12**

![][embedded-image-2]

**Figure: Route Edit**



## Patrol Plan Management

1. On the map settings page, as shown in Figure 13, select **Schedule** from the top menu to open the schedule settings page.  
2. Click the **"+"** button in the upper-right corner to open the schedule settings dialog, as shown in Figure 14.  
3. In the dialog, use the **Select a route** section in the upper-right corner to add inspection routes, and preview the selected routes on the left. Then enter the inspection plan name, select the enabled weekdays, and set the start time, end time, and inspection interval. Finally, choose whether to return Home after completion. After you click **Save**, the system will start executing the inspection plan according to the settings.  
4. After the inspection plan is configured, it will appear in the list as shown in Figure 15, with a summary of the inspection information. You can also click the Enabled field to switch between Active and Inactive, and click Edit to edit or delete the plan, as shown in the plan edit figure.

![][image26]

**Figure 13**

![][image27]

**Figure 14**

![][image28]

**Figure 15**

![][plan-edit]

**Figure: Plan Edit**



# **4. NVR Replay Page**

As shown in Figure 16, select **Replay** from the sidebar to open the replay page.

1. Use the calendar at the top, shown in Figure 17, to select the year and month. Dates with recorded video data are marked with a green check mark.  
2. Select **Single** mode for a specified camera or **Triple** mode for replay.  
3. After selecting a date, the timeline below will mark replayable time ranges in blue, as shown in Figure 18. Move to a blue segment to start replay directly.

![][image29]![][image30]

**Figure 16 / Figure 17**

![][image31]

**Figure 18**

Button descriptions:

| ![][image32] | ![][image33] | ![][image34] | ![][image35] | ![][image36] | ![][image37] | ![][image38] |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Fast Backward | Step Backward | Play | Step Forward | Fast Forward | Zoom Out | Zoom In |

# **5. Logs**

As shown in Figure 19, select **Logs** from the sidebar to open the logs page.

Here you can view AI detection events, emergency events, full inspection task reports, and user action records.

![][image39]

**Figure 19**

## AI Event

As shown in Figure 20, this page lets you view events detected by AI during inspections. You can also use filters to quickly find the information you need and download the report as a PDF.

![][image40]

**Figure 20**

Button descriptions:

| ![][image41] | ![][image42] | ![][image43] | ![][image44] |
| :---- | :---- | :---- | :---- |
| Display images | Show event location | Add filter conditions | Download as PDF |

## Emergency Event

As shown in Figure 21, this page lets you view emergency events for the robot dog, including network disconnections, manual displacement, and unexpected incidents during task execution.

![][image45]

**Figure 21**

## Task Report

As shown in Figure 22, the left side of this page displays all inspection reports executed manually or by schedule. Each report displays a summary, including the inspection name, success or failure status, failure reason if any, elapsed time and battery consumption, number of AI events, and special AI events.

After clicking an inspection report, the right side displays all waypoints and detected event images for that report.

![][image46]

**Figure 22**

## User Action Log

As shown in Figure 23, this page lets you view user operation activities in the system.

![][image47]

**Figure 23**

# **6. Health**

As shown in Figure 27, this page displays the system health status, including the following information:

1. **Server status**
2. **CPU usage**
3. **Memory usage**
4. **Swap usage**
5. **Disk usage**
6. **Motor temperatures**
7. **Network read/write speed**

![][image51]

**Figure 27**

# **7. Settings**

After entering Settings, sub-options are available at the top, as shown in the figure.

![][embedded-image-3]

1. General

On this page, you can configure system settings and license settings. Under System, you can configure maps, upload maps, and upload preset sound effects. Under License, you can update license information.

![][embedded-image-4]

2. AI

On this page, you can configure emergency AI events. Emergency AI events can be displayed as a group in filters.

![][embedded-image-5]

3. Notifications

On this page, you can configure notification items, including:
1. Telegram: Enter your **Telegram ID** in the **Telegram Subscribers** field.
2. Email: Enter the **Email Receiver Address List**, **Sender Address**, and **Sender Password**.

![][embedded-image-6]

4. Engineering

Internal settings. You usually do not need to configure this item.

5. User

You can manage users here. After clicking Action, you can delete a user, modify user information, or change a user's password.

![][embedded-image-7]

[goal-edit]: images/goal-edit.png
[image1]: images/image1.png
[image2]: images/image2.png
[plan-edit]: images/plan-edit.png
[image3]: images/image3.png
[image4]: images/image4.png
[image5]: images/image5.png
[image6]: images/image6.png
[image7]: images/image7.png
[image8]: images/image8.png
[image9]: images/image9.png
[image10]: images/image10.png
[image11]: images/image11.png
[image12]: images/image12.png
[image13]: images/image13.png
[image14]: images/image14.png
[image15]: images/image15.png
[image-init-pose]: images/image-init-pose.png
[image-edit]: images/image-edit.png
[image16]: images/image16.png
[image17]: images/image17.png
[image18]: images/image18.png
[image19]: images/image19.png
[image20]: images/image20.png
[image21]: images/image21.png
[image22]: images/image22.png
[image23]: images/image23.png
[image24]: images/image24.png
[image25]: images/image25.png
[image26]: images/image26.png
[image27]: images/image27.png
[image28]: images/image28.png
[image29]: images/image29.png
[image30]: images/image30.png
[image31]: images/image31.png
[image32]: images/image32.png
[image33]: images/image33.png
[image34]: images/image34.png
[image35]: images/image35.png
[image36]: images/image36.png
[image37]: images/image37.png
[image38]: images/image38.png
[image39]: images/image39.png
[image40]: images/image40.png
[image41]: images/image41.png
[image42]: images/image42.png
[image43]: images/image43.png
[image44]: images/image44.png
[image45]: images/image45.png
[image46]: images/image46.png
[image47]: images/image47.png
[image48]: images/image48.png
[image49]: images/image49.png
[image50]: images/image50.png
[image51]: images/image51.png

[embedded-image-1]: images/embedded-image-1.png
[embedded-image-2]: images/embedded-image-2.png
[embedded-image-3]: images/embedded-image-3.png
[embedded-image-4]: images/embedded-image-4.png
[embedded-image-5]: images/embedded-image-5.png
[embedded-image-6]: images/embedded-image-6.png
[embedded-image-7]: images/embedded-image-7.png
