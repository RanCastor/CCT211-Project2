# About
We have developed a graphical user interface (GUI) for recording student information related to academic and financial queries akin to the University of Toronto's AskRegistrar system (University of Toronto, 2018).

# How to Use Our Application
The form on the left can be filled out to record an individual student entry. Before pressing "Submit", please ensure you have also checked off the form sections "Year of Study" and "Accessibility". When the form is filled out and "Submit" has been pressed, you will see a record of the student's information appear in the table in the top right of the screen. When clicking on an entry, the summary of the message will also appear in the text box below. To edit an individual record, please click on the row holding the student record in the table, and then click on the "Edit" button on the bottom right of the screen. A dialog box will appear that prompts you to verify that you would like to edit the entry. If you click "Yes", the form on the left will automatically fill with the information that was submitted in the last instance it was saved into the database. When the desired edits are made, please click on "Save Changes". Your new changes will now appear in the table. 

# Overview of Design Strategy
The Software Development Life Cycle (SDLC) is a process that advocates for a "framework"-led approach to the management of a team-wide software application, guided by "7 phases" (Swersky, 2022). We apply this strategy in our work to ensure linearity in the pace at which our project evolved from the ideation and discussion stages, to working build in Python.

Requirements entail the expectations of the business for the final product (Swerksy, 2022). In our situation, we were led by the expectations of Professor Michael Nixon as outlined on the CCT211 Quercus shell as well as in lecture. We synthesized these requirements as three separate categories: prioritizing usability and functionality in the planning, design and prototyping stages, testing our product across macOS and Microsoft Windows platforms, and maintaining operations through a central repository system on GitHub.

We will walk through how we addressed some SDLC principles central to our project.

## Planning
The "planning" stage is focused on deliberating on coding techniques and modes of communication, as well as speculations of the design pipeline itself, as a team (Swersky, 2022). 

As a team, we first decided on Discord as a primary mode of teamwide communication. We first quickly planned a time for a preliminary meeting to discuss the scope of this project, which was at first a project proposal. We arrived at the following decisions during this meeting: work on a student record bookkeeping system for exam registration where there is a form in which student information is entered, and on the right of this form should be at least one way to view the student information that was entered. 

## Design and Prototyping
"Design and prototyping" is a stage wherein the team must work from "established patterns for application architecture and software development" (Swerksy, 2022). In this stage, we recognized that we should come up with some visual representations of our ideas, particularly using Figma to create prototypes to arrive at a consensus in terms of design of our GUI. We recognized that it was susceptible to change, ancipated through the expected feedback we expected receiving from feedback from the professor following our proposal submission.

In our first meeting, we discussed our ideas and thoughts on the project. We generated a few sketches:

![design_and_prototyping_1](https://github.com/RanCastor/CCT211-Project2/assets/154641312/737c75d9-54fb-4957-9597-5a9549b96a77)


Working off of these sketches, our blueprint formed via Figma (note: with Dr. Nixon's permission, we have put this screenshot in, which was initially submitted in our proposal):

![design_and_prototyping_2](https://github.com/RanCastor/CCT211-Project2/assets/154641312/4a660852-e757-41f2-9e88-4985885aa456)


Upon receiving feedback from Dr. Nixon, we were recommended to shift the context of our idea towards a AskRegistrar-like system (University of Toronto, 2018) due to concerns about believability, as we learned that exam attendence requires no more than a student number. We changed our form to accept questions from students instead, categorized under the same topics as AskRegistrar, namely "Registration", "Finances", "[T]ransfer [C]redit", "Personal information", "Petition[s]", "Graduation", "Exam Identification", and "Absence Declaration" (University of Toronto, 2018). 

Our project uses Python's modules tkinter, ttk's treeview, sys, datetime, tkcalendar as well as sqlite3.

(view on Mac)
![design_and_prototyping_view_on_mac_1](https://github.com/RanCastor/CCT211-Project2/assets/154641312/faaf1fb9-078d-4963-85d4-60da1a7ecdbf)


Which evolved further (view on Mac):
![design_and_prototyping_view_on_mac_2](https://github.com/RanCastor/CCT211-Project2/assets/154641312/f35237d1-bcd0-435c-b983-30aa2ebcb353)

### Usability
Aside from debugging and code organization as mentioned in the requirements, we further investigated what usability actually entails in a software application. We concluded that ease of use and aesthetics are key to a user interface; it must be easy to look, and easy on the eyes. 

Out of these "15 principles" (Haque, 2023, para 1), we concentrated on __"accessibility"__ (Haque, 2023, para 9), __"clarity"__ (Haque, 2023, para 11), __"simplicity"__ (Haque, 2023, para 17), and __"effectivity"__ (Haque, 2023, para 34). 

One way that accessibility was addressed was through ensuring contrast is adequate. One method is to determine contrast ratio of the colors on the interface. Using the WebAim Contrast checker with colors that roughly map to the ones on a Mac PC as well as a Windows PC, respectively. Firstly, for the Mac PC, we were able to identify that one of the two main interface colors: "#ececec" (_Tk differences on Mac OS X_., n.d., para 20). We had to guess the second color at approximately #383838.

Courtesy of WebAim (n.d.), we were able to confirm that our interface passes the contrast check:
![usability_webaim](https://github.com/RanCastor/CCT211-Project2/assets/154641312/90eb9d2c-d7aa-4bbc-924a-fa2ac91d3d5d)

From here, we could also segment the color usages, primarily "[large text]", which is the "active" text on the UI  (Eggbert et al., 2023a, para 2), and "[incidental]" text, which is the text that is "inactive", the latter of which contrast checking does not apply (Eggbert et al., 2023a, para 3). Additionally, we also ensure that our widgets that require text entry are met with input validation (Eggbert et al., 2023b, para 2), and "labels" (Eggbert et al., 2023b, para 3). 

With respect to clarity, which refers to how obviously identifiable our buttons are (Haque, 2023, para 11), we were able to space out widgets and add padding to text in buttons to make them stand out. Clarity also supports simplicity (Haque, 2023, para 17).

Finally, while this list is not exhaustive, we prioritize effectivity, which refers to the speed of use of this interface to reach a "desired" outcome (Haque, 2023, para 34), by spending no time on transitions and the pace at which input validation is rendered visible on-screen, to ensure the user has a straightforward, seamless user experience in keeping track of each student.

### Functionality
We referred to CRUD, that is, create, record, update, and delete, as a functionality pipeline for this project. We have numerous widgets that help supoort the "create" aspect of this pipeline:
* EntryField
* Combo
* RadiobuttonField
* ScrolledTextWidget
* Three frames on the main UI, housing the form, and the directory as well as individual student question via frame-witching functionality, respectively
* A pop-up window housing editing functionality of individual student records

For the record aspect, we use SQL for our choice of persistence to store each entry's information collected.

For the update aspect, clicking on an individual existing entry displayed in the ttk treeview and then clicking on the "Edit" button first opens a dialog box prompting the user to select an action: confirm their choice to edit the entry, or cancel the request. If the user chooses to confirm, the form on the left will automatically fill up with the last saved information of the entry, from which any edits can be saved and stored in the database.

For the delete aspect, clicking on an individual existing entry displayed in the ttk treeview and then clicking on the "Delete" button first opens a dialog box prompting the user to select an action: confirm their choice to delete the entry, or cancel the request. If the user chooses to confirm, the entry will be erased from the database and simultaneously, from the treeview.

### Organization Logic
Among our widgets, the use of the textbox underneath the table of student records to show the corresponding question easily when a record is clicked, as well as a horizontal scrollbar on the table itself to view all of the data entered for each student without making the table excessively wide. In addition, we ensure that all buttons associated directly with actions that transpire in the form are placed on the side of the form/on the left, namely "Submit" for a new entry, as well as "Save Changes" and "Back" during the editing stage for saving edits and canceling edits, respectively. Likewise, all buttons associated with actions that are instantiated via the table are placed underneath the textbox which is under the table on the right, such as "Delete" and "Edit" for deleting a student's record as well as entering the editing stage after clicking on a record.

## Testing
Through the repository, we were able to view how the interface looks and behaves on both Windows and Mac PCs. This way, we could catch errors.
For example, we addressed the issue with this button's appearance which differed between Mac and Windows (first and second screenshot, respectively):

![testing_submit_1](https://github.com/RanCastor/CCT211-Project2/assets/154641312/d25458d5-346a-4ede-be32-6c8d69a22c3c)

![testing_submit_2](https://github.com/RanCastor/CCT211-Project2/assets/154641312/7a885ecf-f957-4672-b7e1-53f50009b0bf)


We realized that some buttons may sometimes need to be set wider than what seems fine on Mac PCs, to avoid compromising visibility of interface widgets on Windows.

Additionally, the screen used to be cut off for square-shaped monitors. As such, we opted to limit the categories that could be immediately visible in the directory.

![testing_3_view_of_interface](https://github.com/RanCastor/CCT211-Project2/assets/154641312/c1f10f24-d93c-4d00-8e2a-6a4d1d20aee1)

Resolving these errors greatly supports cross-platform compatability in our work.

## Operations and Maintenance
We use GitHub to commit change and make pull requests, but not before clearly communicating with the team that we intend to. This way, we are able to avoid unexpected conflicts that could otherwise jeopardize the integrity of existing files in our repository.

# References
Eggert, E., Abou-Zahra, S., Vanderheiden, G., Guarino Reid, L., Caldwell, B., Henry, S.L., & Lemon, G. (2023a). _1.4.3
Contrast (Minimum) Level AA_. W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/quickref/#contrast-minimum

Eggert, E., Abou-Zahra, S., Vanderheiden, G., Guarino Reid, L., Caldwell, B., Henry, S.L., & Lemon, G. (2023b). _Guideline 3.3 - Input Assistance_. W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/quickref/#reading-level:~:text=Guideline%203.3%20%E2%80%93%20Input%20Assistance

Haque, M. (2023). _15 Most Important Usability Principles for User Interface Design_. Medium. https://medium.com/@mdmansurulhaques/15-important-usability-principles-for-user-interface-design-ea819cedeb36#:~:text=It%20includes%20factors%20such%20as,and%20without%20too%20much%20difficulty

Nixon, M. (2024). _Project 2: Persistent Form_. Quercus. https://q.utoronto.ca/courses/331282/assignments/1174679

Swersky, D. (2022). _The SDLC: Popular models, benefits & best practices_. Raygun. https://raygun.com/blog/software-development-life-cycle/

_Tk differences on Mac OS X_.(n.d.). Tcler's Wiki. https://wiki.tcl-lang.org/page/Tk+differences+on+Mac+OS+X

University of Toronto (2018). _AskRegistrar - Connect With Us_ [Web-Hosted Computer Software]. https://uoft.service-now.com/utm_askregistrar?id=access_sc_cat_item&sys_id=b9ea9cbf1b05b0102d01fc87dc4bcb7d

WebAim. (n.d.). _Contrast Checker_. [Web-Hosted Computer Software]. https://webaim.org/resources/contrastchecker/
