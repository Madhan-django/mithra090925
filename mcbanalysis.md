# **MyClassboard (corp53) — Menu & Page Analysis** 

Oct 30, 2026 · @Madhankumar D 

## **Overview** 

MyClassboard (MCB) for Alpha Group of Institutions (corp53.myclassboard.com) has 71 modules across 8 suites; 47 are active and 24 are locked add-ons. The 47 active modules hold 855 menu pages (after removing mobile-menu duplicates), and many pages carry further sub-tabs. This doc is meant as a functional spec for rebuilding the same scope in Django. 

|Item|Value|
|---|---|
|Login role analysed|SysAdmin (organisation level)|
|Branches|4 — Alpha School (CIT Nagar), Alpha Matriculation Hr. Sec. School,<br>Alpha School Porur, Alpha International School|
|Academic years|2024-25 to 2027-28 (current 2026-2027)|
|Students on dashboard|3,186 (CBSE 3,045 · State 141)|
|Tech pattern|ASP.NET MVC; module shell page<br>/Home/<Module>plus AJAX<br>partial pages loaded into one content panel (<br>#dvmain)|
|Edition|Standard Edition + LMS Standard Edition — 47 of 71 modules<br>active|



How it was analysed: the module switcher was read for all 71 modules. Each active module's menu tree was extracted, and every menu page was fetched read-only. Headings, labels, inputs, dropdowns, buttons, table columns and tabs were recorded. No form was submitted and no data was changed. 

## **Navigation structure** 

The portal has 3 levels: a module switcher (71 tiles in 8 suites), then a module's top menu groups, then pages. On <mark>/Home</mark> the top bar shows 8 core modules (SIS, HR, Finance, Admissions, Transport, Certificates, Library, Organisation). Inside a module, the top bar is replaced by that module's own menu groups. 

### **Module catalogue (71 modules)** 

|Suite|Active modules|Locked add-ons (not<br>analysed)|
|---|---|---|
|ERP (21)|Organisation, SIS, Inventory, Dynamic forms,<br>Learner Profile, Transport, Login Statistics,|Mobile Apps, Visitor Mgmt,<br>Franchisee, Placements,|
||Certificates,Library,Hostel,Concerns,|Student Council,Infirmary,|



|Suite|Active modules|Locked add-ons (not<br>analysed)|
|---|---|---|
||Achievements, Mentors|RFID, Academic Audit|
|Finance (6)|Finance, School Store, Expenses<br>Management, Finance Intelligence|School Services, PDC<br>Management|
|CRM (3)|Admissions|Admissions Plus CRM,<br>WhatsApp Marketing|
|HR (6)|HR, Staff Wall|Payroll, PMS, Continuous<br>Professional Development,<br>Recruitment|
|Communication (10)|SMS, WhatsApp, Email, Voice Calls, Diary,<br>Announcements, Calendar, Activities and<br>Photo Gallery, Notifications, Student Wall|—|
|Add-ons (5)|—|Alumni Management,<br>SQAA, Automated Alerts,<br>NAAC and NIRF, Digital<br>Document Library|
|Gradebook (9)|CBSE and State, ECA and PET, IB Gradebook,<br>Cambridge Gradebook, Pre School, ICSE<br>Gradebook, Higher Ed, Exam Cell|AI Exam Cell|
|LMS (11)|Assignments, Online Classes, Content<br>Management, Online Exams, Baseline<br>Analysis, Reflections, Subjects Management,<br>Class Room Observation, Learning Taxonomy|JEE MAINS, G Suite|



### **Menu groups per module** 

|Module|Menu groups (pages)|
|---|---|
|Organisation|Organisation (10) · Manage Menus (9) · Reports (5)|
|SIS|Enrollments (4) · Approvals (2) · Student Contracts (3) · Time<br>Table (1) · Student Groups (2) · Documents (2) · Reports (32)|
|Inventory|Stores (1) · Item Details (5) · Stock Management (4) ·<br>Vendors and Contracts (9) · Asset Management (4) · Reports<br>(9)|
|Dynamic forms|Dynamic Forms (3) · Data Related Form (2) · Student<br>Feedback and Survey Forms (3) · Reports (8)|
|Learner Profile|Student Discipline(2)· Academic Observations(1)· Student|



|Module|Menu groups (pages)|
|---|---|
||Anecdotes (3) · Achievements (1) · Reports (5)|
|Transport|Route Management (7) · Transport Fee (4) · VTS (5) ·<br>Transport Attendance (2) · Route Intelligence (4) · Reports<br>(13)|
|Login Statistics|Login Settings (2) · Password Help (5) · Reports (6)|
|Certificates|Settings (1) · General Certificates (7) · ID Cards (5) · Transfer<br>Certificate (3) · Achievements and Competitions (2) ·<br>Bonafide Letters (2) · Reports (3)|
|Library|Digital Library (1) · Library Settings (10) · Library Assessment<br>(4) · Reports (9)|
|Hostel|Building Detail (2) · Hostel Management (12) · Meals (3) ·<br>Others (3) · Reports (15)|
|Concerns|Concerns (3) · Staff Concerns (2) · Parent Concerns (4) ·<br>Branch Concerns (2) · TC Requests (4) · Reports (4)|
|Achievements|Achievements (3) · Reports (1)|
|Mentors|Reports (1)|
|Finance|Fee Management (16) · Approvals (12) · Concessions (4) ·<br>Collection Reports (20) · Audit Reports (16) · Due Reports<br>(16) · Scholarship (3) · Log (6) · Reports (21)|
|School Store|School Store (11) · Orders (6) · Base Line (4) · Offline<br>Deliveries (2) · Reports (15)|
|Expenses Management|Expense Management (3) · Approvals / Requests (4) ·<br>Reports (10)|
|Finance Intelligence|Intelligence (3) · Revenue Impact (3)|
|Admissions|Enquiries (11) · Pre admission Reports (17) · Documents and<br>Fields (2) · MIS (7) · Approvals (1) · Reports (18)|
|HR|Staff Details (8) · Attendance (7) · Biometric Attendance (9) ·<br>Leaves (9) · Staff Tasks (5) · Reports (20)|
|Staff Wall|Staff Wall (2) · Staff Meetings (2)|
|SMS|SMS (1) · Send SMS (1) · Fee Due SMS (2) · Reports (2)|
|WhatsApp|WhatsApp Account (5) · WhatsApp (Haptik) (5) · WhatsApp<br>Custom (1) · Attendance (4) · Login Details (1) · Fee Due (1) ·<br>Others(6)· Communication(4)· Two-Waycommunication|



|Module|Menu groups (pages)|
|---|---|
||(3)|
|Email|Email Templates (8) · Send Email (4) · Fee Due Emails (2) ·<br>Reports (3)|
|Voice Calls|Click to Call (2) · Voice Message (5) · Reports (2)|
|Diary|Diary (2) · Reports (2)|
|Announcements|Announcements (4) · School Policies and Student Handbooks<br>(1) · Reports (1)|
|Calendar|Calendar (3) · Birthday Calendar (2)|
|Activities and Photo Gallery|Activities and Photo Gallery (6)|
|Notifications|Template Based Notifications (3) · Attendance Notifications<br>(1) · Notification (2) · Reports (1)|
|Student Wall|Student Wall (5)|
|CBSE and State|Grade Book (7) · Settings (5) · Subject Outcomes (4) · Other<br>Exams (4) · Competitive Exams (3) · Reports (19)|
|ECA and PET|Extra-Curricular Activities (4) · Health (1) · PET (4) · Reports<br>(1)|
|IB Gradebook|Subjects (2) · GradeBook (6) · Attributes (3) · ATL Skills (2) ·<br>Subject Outcomes (4)|
|Cambridge Gradebook|Subjects (1) · GradeBook (6) · Subject Outcomes (4)|
|ICSE Gradebook|Subjects (1) · GradeBook (6) · Subject Outcomes (4)|
|Pre School|Manage Curriculum (6) · Learning Based Assessment (3) ·<br>Child Care Activities (3) · Reports (1)|
|Higher Ed|Grade Book (10) · Outcomes (5) · Reports (1)|
|Exam Cell|Before Exam (9) · During Exam (4) · After Exam (1)|
|Assignments|Assignments (5) · Reports (3)|
|Online Classes|Online Class Management (1) · SyncUp (3)|
|Content Management|Learning (4) · Question Bank (3)|
|Online Exams|Online Exams (5) · Reports (2)|
|Baseline Analysis|Baseline Analysis (2)|
|Reflections|Subject Reflections(1)|



|Module|Menu groups (pages)|
|---|---|
|Subjects Management|Subjects (6) · Content Planners (2)|
|Class Room Observation|Teacher Observations (3) · Class Room Recordings (1)|
|Learning Taxonomy|Blooms Taxonomy Tests (3) · Chapter-wise Diagnostic<br>Assessments (4) · Topic-wise Diagnostic Assessments (1)|



Header utilities (every page): organisation name + logo, AY chip with year switcher (2024-25 to 2027-28), What's New, help/support, module switcher, global search, user menu (Change Access Level, Settings, Change Password, Change MPIN, Analytics and AI Data Insighters, Mobile App Logins, Biometric / RFID / VTS / PG, Security Settings, Logout). 

## **Design system (captured)** 

The UI is Bootstrap 5 with the Lexend font, a white top bar and light-grey canvas, rounded white cards and green filter labels. Values below are read from the live CSS. 

|Token|Value|Where used|
|---|---|---|
|Font family|Lexend (Google Font)|Everywhere|
|Base text|14px / weight 300, #676A6C|Body, navbar links|
|Page title|22px / 400, #6A6A6A|Page header, e.g. "Assign<br>Fee To Student"|
|Form label|14px / 500, #198754 (Bootstrap success green)|Filter and form labels|
|Primary button|#005BE8 bg, white text, 13px, radius 3px, ~30px<br>high|Get Students, Search,<br>Submit|
|Outline button|#1C84C6 text and 1px border, transparent bg, radius<br>3px|Secondary actions in the<br>page header|
|Inputs / selects|White, radius 6px, Select2 searchable dropdowns|All filters|
|Card|White, radius 16px, 1px border rgba(11,11,11,.1),<br>shadow 0 1px 2px rgba(11,11,11,.04)|Dashboard KPI tiles and<br>panels|
|Top bar|White, 75px high, shadow 0 2px 4px<br>rgba(0,0,0,.075), orange accent line under it|Global header|
|Org name|Orange-red, semi-bold|Header title|
|Dropdown menu|#F5F5F5 bg, 12px items, radius 3px, multi-level<br>flyouts|Module menus|
|Active tab|Coral/red underline|Dashboard tab strip|



|Token|Value|Where used|
|---|---|---|
|Breadcrumb bar|Dark (near-black) strip, white text: Module › Group ›<br>Page, with video-help, info and help icons on the<br>right|Every module page|
|AY chip|Pale lilac pill, "AY: 2026-2027"|Header|



### **Page anatomy (same on almost every page)** 

1. Header: logo, organisation name, module menu bar, then on the right the idea/bookmark/support pill, AY chip, store icon, search, module switcher button and avatar with role (SysAdmin). 

2. Breadcrumb strip (dark) with help icons. 

3. Page title on the left; secondary outline buttons on the right (e.g. Assign On Demand Fee, Assign Lunch Fee, Assign Transport Fee). 

4. Filter card: 4-column grid of labelled Select2 dropdowns (Academic Year, Branch, Class, Section, plus page-specific filters), primary action button at the end of the last row. 

5. Results area: a data table with column headers, export buttons (Excel/PDF/Print) and row actions; reports follow the same filter → Get → table flow. 

6. Footer: support phone, email, policy links. 

### **Module switcher** 

A right-side drawer titled "Search 71 modules": left column lists suites with counts (ERP 21, Finance 6, CRM 3, HR 6, Communication 10, Add-ons 5, Gradebook 9, LMS 11, Available to add 24). The right side shows icon tiles grouped by suite; locked tiles are greyed with a padlock. The footer shows edition progress ("47 of 71 modules active") and an upsell button. 

For Django: use Bootstrap 5 + Lexend, Select2 (or Tom Select) for filters, and HTMX <mark>hx-get/hxtarget="#main"</mark> to copy the AJAX-partial navigation pattern. 

## **Home dashboard** 

The organisation dashboard ( <mark>/Home</mark> ) has 9 tabs; the Dashboard tab is an overview of KPI cards and panels for the selected academic year ("Data as on 30 Oct 2026"). 

|Tab|Content|
|---|---|
|Dashboard|KPI cards + panels (below)|
|Branches|Branch-wise strength, Day Wise / Month Wise toggle; strength "as<br>on selected month or date"|
|Enrollment Review|Enrollment review by branch/class (loads via AJAX)|



|Tab|Content|
|---|---|
|Students M-o-M|Month-on-month student strength|
|Room Allocations|Classroom/room allocation view|
|Email Notifications|Event → recipient matrix: 9 events in 4 categories (Communication<br>1, Requests & Approvals 4, Reports & Data 2, Feedback 2); KPIs<br>Configured events, Unique recipients, Also auto-notified (Branch<br>Principal, Zonal Head), Possible duplicates; read-only for non-<br>support roles|
|Email⚙|Email settings|
|Classes in progress|Live timetable periods running now|
|Principal Diary|Principal's diary entries|



Dashboard tab widgets: 

|Widget|What it shows|
|---|---|
|Students|Total 3,186 "across 2 boards"|
|Total Staff|270; 231 Permanent; new joinees in last 7 days|
|SMS Credits|368, Sender ID ALPHAI; Recharge, Usage, DLT links|
|Inventory Items|Categories · sub-categories · types counts|
|Students by board|Filter chips All / CBSE / State, then bars by stage (Pre Primary,<br>Primary, Secondary, Higher Secondary, Sr Secondary State);<br>"Data Checker" link|
|Staff overview|Teaching 218 of 254 permanent (86%), Non-teaching 13 of 16<br>(81%), Transport 0, Total 231 of 270 (86%); split by Temporary /<br>Permanent / Part-time / Probation; "Hierarchy" link|
|Concerns|Today / 7 days / 30 days toggle; Parent, Staff, Inter-office<br>concern counts|
|Board-wise branch count|Branches per board; "Strength" link|
|Communication|SMS / Voice / WhatsApp / Premium tabs with credits and plan<br>links|
|Login status|Login Status and Never Logged-in List|



The user menu shows school code, edition (ERP: Standard Edition, LMS: LMS Standard Edition) and links to Security Settings and Logout. 

## **Master data and core entity forms** 

These are the records every module hangs off. They were read from the live edit forms, recording field names only and no personal values. 

### **Branch settings (per branch × AY)** 

|Block|Fields|
|---|---|
|Login defaults|Login URL, default student username (Enrollment code), parent<br>username (p_Enrollmentcode), alias usernames, default password<br>(Enrollment code)|
|Basic settings|Current AY, Pre-admission AY, State, City, AY months on/off, Branch<br>type (School / College / Pre-school), Organisation SMS sender ID,<br>Enrollment code prefix, Branch SMS sender ID, Branch short code,<br>Biometric device (Y/N), VTS device (Y/N), Receipt type (Online /<br>Manual, auto-generated)|
|Principal|Name, username, mobile, email (multiple)|
|Class teachers|Class × Section → class teacher(s): name, username, mobile, email.<br>Sections include A–D plus "New Admission" and "New Admission<br>(Provisional)" holding sections|
|Counsellors|Front-office users; flags Allow direct admission, Allow payment<br>while admission|
|Accountants|Name, username, mobile, email|
|Fee plan availability|Per class: New students Y/N, Existing students Y/N|
|Fee accounts|Fee account name + receipt prefix (e.g. school trust, society,<br>training company — 3 per branch)|



Class ladder in use: Pre KG, LKG, UKG, Grade I–X, Class XI / XII Science, Class XI / XII Commerce. Boards: CBSE, State. 

### **Student profile (13 edit sections)** 

|Section|Fields|
|---|---|
|Enrollment|First, Middle, Last name; Gender; DOB; Date of<br>admission; Email; Mobile (+ country code); Admission<br>type (Day scholar / Residential / Semi-residential /<br>Weekly boarder / Residential with AC); Student segment;<br>Quota (General / Management); Regular / Lateral|
|Personal|Religion, Caste (BC/OBC/OC/SC/ST…), Sub-caste, Mother<br>tongue,Bloodgroup,Nationality,Citizenship (Citizen/EP|



|Section|Fields|
|---|---|
||/ DP / S-Pass / PR), Residence phone, Last school studied,<br>Resident status, Aadhaar no, Qualified exam rank, Eligible<br>for scholarship, Identification marks 1–2|
|Place of birth|Place, Village, District, Country, State|
|Parents|Parental status (Biological / Adoptive / Divorced /<br>Widow / Legal guardian…), Child custodian, Point of<br>contact (Father / Mother / Guardian / Both). Father &<br>Mother each: name, mobile (+code), qualification,<br>organisation, designation, occupation (Business / Farming<br>/ Govt / Pvt…), company (master list), Aadhaar, email,<br>alternate email, DOB, citizenship, nationality, mother<br>tongue, blood group; Marriage anniversary|
|Guardian|Name, mobile, occupation, email, alternate email, point<br>of contact|
|Siblings|Sibling 1 & 2: name, enrollment code, occupation, mobile|
|Address|Current address, nearest locality (Google autocomplete),<br>country, state, city, latitude, longitude; same-as-current<br>checkbox; permanent address block|
|Identity (student, father, mother)|Passport no, issue place, validity, issue date; Visa no,<br>issue date, expiry; PAN; Aadhaar|
|Reference codes|Admission/Reference code, GR / EMIS / STS / ESIS no,<br>Roll no, Student unique code + issue/expiry, Smart card<br>no, State govt no, Father/Mother unique code + dates,<br>Electricity account, Water account, Family ID, Parent ID|
|Govt IDs|Student PEN, Father PEN, Mother PEN, Student APAAR ID|
|Documents checklist|Yes / No / NA for: Birth certificate, TC, Immunisation<br>record, Photos (student, father, mother), Previous report<br>card, Blood group report, Health certificate, Transport<br>policy, Address proof, 10th / Intermediate certificate,<br>Application form, School policy, Caste certificate, Age<br>undertaking, Resource form, Discount form, Photo<br>release form|
|Pre-admission documents|Uploaded files from the admission stage|
|Missed mandatory fields|Prompts for any field marked mandatory but empty (e.g.<br>Father/Mother Aadhaar, Mother DOB)|



Student list grid: Student, Enrollment code, GR No, Class · Section, How they joined, Date of admission, Age (DOB), Point of contact, Last attended, Status, Actions (Edit, Leadership responsibility, Request inactive, Suspend). Status tiles: Active / Inactive / Suspended. 

### **Staff profile** 

|Section|Fields|
|---|---|
|Quick add (Staff Admit)|Staff type (Teaching / Non-teaching), Department, Designation,<br>Access level, Name, DOB, Gender, Mobile, Date of joining, Email|
|Basic|Staff type, Salary type (Consolidated / Scale), First / Middle / Last<br>name, DOB, Married, Gender, Place of birth, Home town,<br>Qualification, B.Ed, M.Ed, Specialisation, Nationality, Religion,<br>Citizenship, Govt ID / Resident no + validity, Aadhaar, PAN,<br>Annual family income, Identification marks 1–2, Blood group,<br>Height, Weight, Physical disabilities|
|Contact|Address, Landmarks 1–2, Country, State, City, PIN, Official email,<br>Personal email, Mobile, Alternate, Emergency, WhatsApp (with<br>country codes)|
|Bank & statutory|Bank account, IFSC, Bank name, Branch, City, State, EPF no,<br>UAN, ESI no, Medical insurance issuer + no, Driving licence +<br>validity, Passport + validity|
|Payroll|Payroll entity, Payment type (Online / Cheque / Cash), Salary pay<br>type|
|Academic role|CTET qualified + score, Trained as (TGT / PGT / PRT / NTT / PET),<br>Class category, Subjects 1–3|
|Assignment|Your branch / Multiple branches, Branch, Biometric code,<br>Department, Outsource flag, Staff reference code, Designation,<br>Reporting level + reporting to|
|Family|Relationship, Full name, Contact, DOB, Age, Occupation, Staying<br>with me|
|Remarks|Date, Remarks, Zonal head remarks|



Related masters: Qualification, Designation, Department, Staff groups, Shifts, Outsourcing vendors; staff documents, NOC, exit form, resume. 

### **Fee structure (as configured)** 

Fee Type (e.g. Consolidated school fee, Grade Eligibility Fee, Transport Fees) → Fee Plan per class and per New / Existing (e.g. "School Fee LKG", "School Fee LKG (New)", transport slabs "0–3 km", "3.1–6 km", "6.1–9 km") → amount and installments → assigned to students. The receivables grid shows Class, 

Section, Active / Inactive, Existing / New / Total, Fee plan, Plan assigned strength, Fee type, Type assigned strength, Amount, Projected amount. 

## **Module-by-module page analysis** 

Every menu page of the 47 active modules is listed below with its endpoint, inputs, actions and output columns. Most pages follow one pattern: filter dropdowns, then a Get / Show Report button, then a table or tabbed sub-views. 

Abbreviations: AY = Academic Year, Br = Branch, Cls = Class, Sec = Section, DR = date-range dropdown (Today / Last 7 days / Last 30 days / Date Range / Till Date) with start and end date inputs. “Tabs” are sub-views inside the page; each tab is effectively its own sub-page. 

### **Organisation** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Organisation ›<br>Branch Settings|/Organisation/<br>BranchSettingDashBoar<br>d|AY, Br|Get → branch settings<br>dashboard|
|Organisation › Get<br>Started|/Organisation/<br>OrginasitionDefaultSte<br>ps|AY (2009-10 onward),<br>Br|Get → setup checklist ("Get<br>Start Steps")|
|Organisation ›<br>Manage Admin<br>Users|/Organisation/<br>CreateUser_New|—|Tabs: Organisation, Zonal,<br>Branch admin users|
|Organisation ›<br>Invoices|/Organisation/<br>ZOHOInvoices|Financial Year|Tabs: Due Invoices, Paid<br>Invoices, Receipts, Pay<br>Online Class Invoices. Cols:<br>Billing Account No, Name,<br>Service Type|
|Organisation ›<br>Support Tickets List|/Organisation/<br>Getzohotickets|Financial Year|Get, Tickets Summary|
|Organisation ›<br>Daily Feedback|/Organisation/<br>FeedBackMaster|—|Shows Student Feedback<br>Link|
|Organisation ›<br>Hardware Scan|/Report/<br>RptDeviceLogReport|Br, Device ID, Date|Tabs: Biometric, RFID, RFID<br>Transport, VTS, VTS+RFID<br>data logs, SMS DLT<br>Activations, PG Activations.<br>Help-request buttons per<br>integration|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Organisation ›<br>Manage Branch<br>Staff Users|/Organisation/<br>ManageStaffSettings|Br, Staff Department|Get → staff login settings|
|Organisation ›<br>Manage User Type<br>Modules|/Organisation/<br>ManageUsertypeWise<br>Modules|—|Tabs: Organisation, Zonal,<br>Branch, Staff — module<br>access per user type|
|Organisation ›<br>Organisation FAQ's|/Student/<br>OrganisationFAQs|FAQ Type<br>(Web/Android/iOS),<br>Question, Answer<br>(manual or file upload)|Save. Cols: S.No, Question,<br>Answer, FAQ Type, Action|
|Manage Menus ›<br>Student/Parent<br>Mobile App Menus|/Menu/<br>MobileAppMenus|Menu Name, Title, Nav<br>URL, Priority|Tabs: Student Login Menus,<br>Parent Login Menus,<br>Mobile App Banners, App<br>Advanced Settings.<br>Create/Edit Menu and Sub<br>Menu modals|
|Manage Menus ›<br>Organize Menus|/Menu/<br>GetAssignMenuByOrga<br>nisationID|Role, Menu group<br>(ERP/Finance/Grade<br>Book/Connect/LMS)|Manage Modules — per-<br>role menu assignment|
|Manage Menus ›<br>Parent/Student<br>Web Menus|/Menu/<br>ManageParentandStud<br>entWebMenus|—|Tab: Parent/Student Login<br>Menus|
|Manage Menus ›<br>MCB SMART<br>SCHOOL App<br>Menus|/Menu/<br>TeacherAppmenusAssi<br>gn|Access level<br>(Organisation/Zone/Br<br>anch/Staff/Class<br>Teacher), User Type|Get → teacher-app menu<br>toggles|
|Manage Menus ›<br>Branch Staff<br>dashboard web<br>Menus|/Menu/<br>ManageStaffMenus|Checkbox grid|Bulk Save. Cols: Menu<br>Name × roles (Staff, Class<br>Teacher, Front Office,<br>Librarian, Sr. Admission<br>Counsellor & HR, Transport<br>Incharge, ERP, Senior<br>Administrator)|
|Manage Menus ›<br>SMART SCHOOL<br>App Profile Menus|/Menu/<br>TeacherAppmenusAssi<br>gn_New|User Type, Access Level|Get|
|Manage Menus ›|/Menu/|User Type, Access Level|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|SMART SCHOOL<br>App Approval<br>Menus|TeacherAppmenusAssi<br>gn_New|||
|Manage Menus ›<br>Curriculum based<br>LMS Modules|/Menu/<br>CurriculumBasedLMSM<br>odules|Br|Get|
|Manage Menus ›<br>Student/Parent<br>App Profile Fields|/Organisation/<br>UserTypeFields|~50 field checkboxes|Save. Sections: Academic<br>Details, Student, Parent<br>Details (Enrollment Code,<br>Admission No/Date, Roll<br>No, Board, Aadhaar, PAN,<br>PEN, APAAR, DOB, House,<br>Transport, Blood Group,<br>Photo, Segment, Hall<br>Ticket, Gender, Religion,<br>Caste,<br>Father/Mother/Guardian<br>name-phone-email,<br>Address…)|
|Reports › User type<br>wise Menus|/Organisation/<br>OrganizeMenus_Repor<br>t|Access level, Menu<br>type (ERP/LMS/Add-<br>ons/Connect/Fin)|Show|
|Reports › Users<br>Feedback|/Report/<br>RptUsersFeedbacksCou<br>nt|Location, Br|Show Report|
|Reports › School<br>Feedbacks|/Report/<br>Reportschoolfeedback|Br, DR|Get|
|Reports › Teacher<br>Compliments and<br>Reviews|/Connect/<br>ReportTeacherfeedbac<br>k|Br, DR|Get|
|Reports ›<br>Organisation MIS|/Connect/<br>ReportModuleWiseCou<br>nts|—|Module-wise usage counts|



### **SIS (Student Information System)** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Enrollments ›|/Student/|AY, Br|Upload students; student|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Student Details|ManageViewStudentLis<br>t||list with profile drill-down|
|Enrollments › Email<br>Syntax Validator|/Subject/<br>StudentEmailSyntaxVali<br>dation|Br, Cls, Sec / Br,<br>Departments|Tabs: Student, Staff email<br>validation|
|Enrollments › Bulk<br>Student Branch<br>Transfer|/Student/<br>BulkBranchShuffleStud<br>ents_New|Current AY/Br/Cls/Sec<br>→ Transfer<br>AY/Br/Cls/Sec|Get, Save; view/add AY<br>start dates|
|Enrollments ›<br>Programme<br>Structure<br>(Professional<br>Colleges)|/Organisation/<br>ProgrammeStructure|Location, Br, AY,<br>Programme Category,<br>Programme/Dept,<br>Batch, Class Name,<br>Priority|Assign Programme Years &<br>Sections, Save. Cols:<br>Programme Category,<br>Programme, No. of Years,<br>No. of Semesters|
|Approvals ›<br>Approve Inactive /<br>Reactive Requests|/Student/<br>ApproveStudentDeletin<br>g|Location, Br, Remarks|Tabs: Pending Request<br>Dashboard, Approve to<br>Inactive, Approve to<br>Reactivate, Overview.<br>Approve / Reject|
|Approvals › Bulk<br>Approve Inactive /<br>Reactive|/Student/<br>ApproveStudentDeletin<br>g_Old|Location, Br, Remarks|Tabs: Inactive, Activate.<br>Approve / Reject|
|Student Contracts ›<br>Existing Students|/FrontOffice/<br>PreadmissionViewDocu<br>mentsandContractDeta<br>ils|AY, Promoted AY, Br,<br>Student Type<br>(All/Existing/New), DR|Tabs: Manage documents<br>& fields to verify, Parent<br>Information Updated Log,<br>Documents Dashboard,<br>Pending verification,<br>Contract forms signed|
|Student Contracts ›<br>Pre admission<br>Students|/FrontOffice/<br>PreadmissionDocumen<br>tsandContractDetails|AY, Br|Tabs: Pre Admission<br>Documents, Completed<br>Application Stage,<br>Concession Pending<br>Approvals|
|Student Contracts ›<br>Student Fee<br>Discount<br>Documents|/Fee/<br>ManageStudentDiscou<br>ntForm|AY, Br, Classes,<br>Sections, Status|Tabs: Fee Contracts,<br>Readmission Contract<br>forms|
|Time Table ›|/Organisation/|Br, AY|Tabs: Timetable Master,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Timetable Structure|GetFullTimeTable||Timetable Structure,<br>Schedule Timetable,<br>Upload Timetable, Day<br>Wise Timetable, Staff Work<br>Load, Period Types (co-<br>curricular/extra), Practical<br>Batches|
|Student Groups ›<br>Manage Student<br>Groups|/Student/<br>ManageStudentClassGr<br>oupDetails|AY, Br, Status;<br>Consolidated / Class /<br>Section wise|Tabs: Academic, House,<br>Finance, SchoolStore,<br>Custom Groups, School<br>Clubs, Extra-Curricular,<br>Project, System Tags,<br>Student Segments|
|Student Groups ›<br>Manage Group<br>Activities|/Student/<br>ManageClubActivitiesD<br>etails|AY, Br, Status|Views: House, School<br>Clubs, Extra-Curricular|
|Documents ›<br>Student Documents|/Followup/<br>PreadmissionExistingSt<br>udentDocumentsDashb<br>oard|AY, Br|Show Report → digital<br>documents dashboard|
|Documents ›<br>Manage Profile<br>photos|/Student/<br>DownloadStudentPhot<br>os|AY, Br, Cls, Sec|Get → bulk photo<br>download/upload|
|Reports › Student<br>Contact Details|/HomeDasboard/<br>StudentAllClsContactD<br>etails|Br, Board, Programme<br>Category, Programme,<br>Year, Cls, Sec,<br>Admission Category,<br>Status, Sort By|Add/Remove Columns<br>picker (~50 fields: IDs, roll,<br>segment, parent<br>emails/phones, birth place,<br>address, nationality,<br>religion, mother tongue,<br>caste, MS/Google emails,<br>previous school,<br>Aadhaar/PAN). Download<br>history table|
|Reports › Branch<br>wise Students<br>strength|/HomeDasboard/<br>GetAllStudentsListDash<br>Board_Index|—|Cols: Location, Branch, Pre<br>KG … Grade X, XI/XII<br>Science & Commerce,<br>Total|
|Reports › Student|/SISDasboard/<br>StudentStrength_Repor|Br|Tabs: Eagle eye, Month-<br>wise closingstrength,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Strength Report|ts_New||Gender wise, Age wise,<br>Class Strength Gap,<br>Siblings, Staff wards,<br>Vacancy report,<br>Admissions & exits|
|Reports › Student<br>Group details|/Student/<br>StudentIndividualWise<br>Report|AY, Br, Cls, Group Type,<br>Status|Get|
|Reports › Shuffled<br>students|/Student/<br>RptBranchShuffledStud<br>ents_Main|Br, AY, Months|Show Report|
|Reports › Sibling<br>Report|/<br>FeeCollectionReports/<br>SibilingDetailsReportFo<br>rmat2|Br, Cls, Sec, Fee Type,<br>Category|Tabs: Sibling Dues,<br>Students without siblings,<br>All Students|
|Reports ›<br>Biometric / RFID<br>Punch Log|/Student/<br>StudentAttendancePun<br>chDetails_Get|Br, Punch Date|Get; Send Absent Message<br>via WhatsApp|
|Reports › Student<br>Segment Report|/Report/<br>StudentSegmentDashB<br>oard|AY, Br, Status|Tabs: Class Wise, Section<br>Wise|
|Reports › Admission<br>Details Report|/<br>FeeCollectionReports/<br>RptAdmissiondts_Melu<br>ha|Br, AY, Cls, Admission<br>entered DR, Status|Tabs: Eagle Eye, Class<br>Wise, Branch Wise,<br>Student full details, with<br>fee, Admitted fee heads &<br>discounts, Sources &<br>localities, Before-<br>admission fee heads|
|Reports › Sub Class<br>Group Report|/Report/<br>RptSubGroupWiseStud<br>entLsitReport|Br, Type<br>(Consolidated /<br>Student wise)|Get|
|Reports › Inactive<br>students|/SISDasBoard/<br>InActiveStudentRollAud<br>it|Br, Cls, Sec|Get|
|Reports › Students<br>Promotion Report|/Report/<br>RptStudentsPromotRep<br>ort|Promoted From AY, To<br>AY, Br, Class Type|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Reports › Date-wise<br>Attendance Not<br>Marked|/organisation/<br>RptAttendanceNotgive<br>ndetailed|Br, Month|Get|
|Reports › Financial<br>Promote Students|/Student/<br>RptGetFinancialPromot<br>edStudents|AY, Br, Cls, Sec, DR|Show Report|
|Reports ›<br>Withdrawal Fee<br>Refund|/Report/<br>StudentFeeRefunds|AY, Br, Status<br>(Rejected/Pending at<br>Principal/Approved),<br>Report type|Show Report|
|Reports › Hobbies<br>and Talent|/Student/<br>HobbiesandTalentRepo<br>rt|Br, Class & Sec, Type<br>(Hobbies/Talent),<br>Person<br>(Student/Father/Moth<br>er/Guardian)|Get|
|Reports › Student<br>Attendance Report|/Report/<br>StudentAttendance_Re<br>ports|Br, Term, Class-Sec|Sub-reports: Monthly,<br>Evaluation wise, Analysis,<br>Term wise, Late Comers,<br>Leave Intimation, Daily,<br>Session wise, Average,<br>Overall|
|Reports › Student<br>Biometric<br>Attendance|/Report/<br>PopulateStudentBiome<br>tricAttendanceDateWis<br>e|Br (biometric), Timings,<br>Cls, Sec, Date|Tabs: Attendance<br>Dashboard, Absent list.<br>Update biometric<br>attendance, Device log,<br>Late report, Lost ID cards,<br>Modified list, Session wise|
|Reports › Student<br>Leave Intimation|/Finance/<br>StudentLeaveIntimatio<br>nsDashboard|Br, DR|Create Student Leave<br>Types, Get|
|Reports › Period<br>Wise Attendance|/Student/<br>StudentAttendancePeri<br>odWiseReport|Br, Cls, Sec, Subject, DR<br>(max 31 days), Format<br>1/2/3|Course-wise, By staff, Day<br>wise|
|Reports ›<br>Professional<br>Students<br>Attendance|/Student/<br>AttendanceReportForP<br>rofessionalStudent|Br, Class-Sec, Days,<br>Date|Tabs: Between dates,<br>Monthly|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Reports ›<br>Examinations<br>Attendance|/Examination/<br>OtherExamAttendateR<br>eportByExamination|Class Group, Cls,<br>Examination|Get|
|Reports › Teaching<br>Staff Activity Log|/Student/<br>GetStaffActivityLogs|Br, Date|Get|
|Reports › Subject<br>Teachers List|/Report/<br>RptSubjectTeachers_St<br>atus|AY, Br, Classes,<br>Subjects|Get|
|Reports › Class<br>Teachers List|/Staff/<br>RptClassTeacherStatus|Br, AY|Show Report|
|Reports › Staff<br>Work Load|/Report/<br>DayStaffTimeTable|AY, Br, Type (Single<br>day/Detailed/Consolida<br>ted), Date|Get|
|Reports › Branch<br>Activity Log|/Report/<br>RptBrachActivityLogRe<br>port|Br, AY, Date, Format<br>(Activity log / Staff<br>tasks)|Show Report|
|Reports › Principal<br>Diary|/Organisation/<br>PrincipalDailReport|Br, Month|Get|
|Reports › Student<br>Data Update Log|/Student/<br>StudentsDataUpdation<br>Log|AY, Br, DR|Get|
|Reports › Student<br>Suspension Log|/Student/<br>Studentsuspensions_R<br>eport|AY, Br, Programme, Cls,<br>DR|Get|
|Reports › Teacher<br>Management Data<br>Change log|/Staff/<br>TeacherManagement_<br>Datalog|Br, DR|Get|
|Reports › Students<br>Strength Audit|/Report/<br>StudentsAdmissionAnal<br>ysisReport|AY, Br|Get|



### **Inventory** 

Item master uses a 4-level hierarchy: Category › Sub Category › Sub Category Type › Item. Stock is held per Store and per Branch, with inward/outward transfers. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Stores › Create Store|/Inventory/<br>InventoryStoresCreation<br>_New|—|Tabs: Store Creation,<br>Assign Stores to Store<br>Incharge, Stock<br>Checking Settings,<br>Store wise signatures|
|Item Details › Create<br>Items|/Inventory/<br>NewInventoryCategories|Category, Sub<br>Category, Type, Item|Tabs: Item Master,<br>Categories, HSN & GST,<br>Stores & Branch<br>Mapping|
|Item Details › Store<br>Stock Details|/Inventory/<br>InventoryItemDetails|Store, Category<br>hierarchy, As on date /<br>DR, Item|Tabs: Consolidated,<br>Detailed. Add / upload<br>items to store stock;<br>Store Stock Transfer|
|Item Details › Branch<br>Stock Details|/Inventory/<br>InventoryBranchStockRe<br>port|Br, Category hierarchy,<br>Status, As on date / DR|Tabs: Consolidated,<br>Detailed. Add / upload<br>items to branch stock|
|Item Details ›<br>Generate Barcodes|/Inventory/<br>InventoryItemBracodes|Category hierarchy,<br>Item, Barcode size<br>(7×3cm, 5×2cm, 3.5cm,<br>9.5cm), Print label<br>(Item / Org name /<br>None), No. of copies|Generate Barcodes|
|Item Details ›<br>Damaged Items Entry|/Inventory/<br>InventoryDamagedItems<br>_Tabs|—|Branch-wise and Store-<br>wise damaged entry +<br>reports|
|Stock Management ›<br>Request for Quotation|/Inventory/<br>InventoryRequestForQu<br>otation|Financial Year, Store,<br>Br, DR|Add RFQ (modal), Get|
|Stock Management ›<br>Purchase Order|/Inventory/<br>InventoryPurchaseOrder|Financial Year, Store,<br>Br, PO DR|Get, create PO|
|Stock Management ›<br>Store Stock Transfer|/Inventory/<br>InventoryStockTransferD<br>etails|Store, As on date / DR|Tabs: Inward, Outward|
|Stock Management ›<br>Branch Stock Transfer|/Inventory/<br>InventoryStockTransferD<br>etails_Branch|Br, As on date / DR|Tabs: Inward, Outward|
|Vendors › Manage|/Staff/|Br|Tabs: Outsourcing|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Outsource Staff|StaffTabwiseSalaryInfo_<br>OutSource||Vendors, Contracts,<br>Map Staff to Vendor,<br>Entity/Pay type|
|Vendors › Vendor<br>AMC Proposal|/Inventory/<br>InvVendorAMCServiceDe<br>tails|Br, Category, Sub<br>Category, Item (fixed +<br>service needed)|Get|
|Vendors › Create /<br>Manage Vendors|/Inventory/<br>InventoryVendorMaster|Br, Verified, Status.<br>Form: Vendor name,<br>code, contact, services<br>(Sales / AMC /<br>Outsource), PAN, credit<br>limit, GSTIN, bank a/c,<br>IFSC, bank, MICR,<br>MSME, address<br>(country/state/city)|Add Vendor, Send mail<br>for documents. Cols:<br>Vendor Code, Name,<br>Contact, Mobile, Email,<br>PAN, GSTIN, MSME,<br>Status, Verified, AMC,<br>Sales, Documents, No.<br>of items, No. of<br>branches|
|Vendors › Manpower<br>Supply Contracts|/Connect/<br>ServiceContractDetails|Br|Get|
|Vendors › Rate<br>Contracts|/Connect/<br>RateContracts_Main|Br|Get|
|Vendors › Contract<br>Approval Settings|/Connect/<br>ManagePurchaseContrac<br>tApprovals_Main|—|Tabs: Service, Rate,<br>Inventory Item<br>Request, AMC, Work<br>Order — approver<br>chains|
|Vendors › Purchase<br>and Contract<br>Approvals|/Connect/<br>PurchaseContractReques<br>ts_Main|Location, Br, Pending /<br>Approved, DR|Get, approve|
|Vendors › Raise<br>Request|/Connect/<br>PurchaseAndContractRe<br>qDetails|Br|Tabs: Service<br>Contracts, Rate<br>Contracts, Inventory<br>Item Request, AMC<br>Contracts, Work Order<br>Request|
|Vendors › Contract<br>Approval Report|/Connect/<br>RptPurchaseContractReq<br>uestsApproves|FY, Location, Br, Status|Same 5 tabs|
|Assets › Asset|/Inventory/|Br, FY|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Purchase Details|GetAssetPurchaseData|||
|Assets › Category<br>Items Assets Mapping|/Inventory/<br>InventoryCategoryItemsL<br>ist|Asset Type, Store, Br,<br>Category hierarchy,<br>Individual / Bulk save|Tabs: Fixed, Current,<br>Tangible, Intangible,<br>Financial, Consumable<br>assets, Asset Mapping|
|Assets › Stock Invoice<br>Inward Details|/Inventory/<br>StockInvoiceInwardDetai<br>ls|Status, Store, PO No.,<br>PO date, Inward date,<br>Delivery challan<br>no/date, Invoice<br>no/date, Vendor|Inward Entry, Save<br>(GRN)|
|Assets › Fixed Assets<br>Management|/Inventory/<br>GetOrganisationAssets|Store, Br|Get|
|Reports › Item wise<br>Sales|/Inventory/<br>TotalInventorySalesrepo<br>rt|AY, Br, DR,<br>Consolidated / Detailed|Get|
|Reports › Staff<br>Inventory Issued Items|/Inventory/<br>GetStaffIssuedItems|Br, Returnable, Staff<br>Status, Returned<br>status, Department, DR|Get|
|Reports › Branch stock<br>Register|/Report/<br>RptBranchStockregister|Store, Br, Category<br>hierarchy, As on / DR|Get|
|Reports › Store stock<br>Register|/Report/<br>RptStoreStockregister|Store, Category<br>hierarchy, As on / DR|Show Report|
|Reports › Month wise<br>Branch stock|/Inventory/<br>InventoryMonthOnMont<br>hOpeningClosingBranchS<br>tockReport|Br, Category hierarchy,<br>Month|Opening/closing stock|
|Reports › Vendor<br>Master Report|/Transport/<br>GetInventoryVendorMas<br>terReport|Location, Br|Show Report|
|Reports › Student<br>Stock Issued|/inventory/<br>StockIssuedFeePaidStud<br>ents|Store, Br, Category,<br>Issued / Not issued, DR|Get|
|Reports › Purchase<br>Order Details|/inventory/<br>InventoryPurchaseOrder<br>_Detials|FY, Store, Br|Get|
|Reports › Groupwise|/Inventory/|AY,Br,Class,Misc Fee|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Sales|RptInventoryKitsSalesRe<br>port|Group||



### **Dynamic forms** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Dynamic Forms ›<br>Student Forms|/Student/<br>StudentRelatedDynamic<br>Forms|AY|Form-builder list for<br>student forms|
|Dynamic Forms › Staff<br>Forms|/Organisation/<br>DynamicStaffForm|AY|Form-builder list for<br>staff forms|
|Dynamic Forms ›<br>Public Forms|/Organisation/<br>DynamicPublicForm|—|Public (no-login)<br>forms, optional<br>payment|
|Data Related Form ›<br>Generate|/Student/<br>GetStudentRelatedForm<br>s|Br, Cls, Sec, Transport<br>(Y/N), Student type,<br>Category, Form, copies<br>per row, spacing|Get Forms. Tabs: Bulk<br>Download, Student<br>Wise Download|
|Data Related Form ›<br>View or Manage|/Student/<br>CreateStudentDataRelat<br>edReport|Location, Br, Format<br>(new/existing), Format<br>Name|Custom Format,<br>Default Templates,<br>Save|
|Feedback & Survey ›<br>Feedback and Survey<br>Forms|/FrontOffice/<br>AnnexuresFeedBackFor<br>m|AY, Rating scale (5/6/7<br>point), Max rating|Manage Rating Scale,<br>Assign. Cols: Rating,<br>Description, Image|
|Feedback & Survey ›<br>General Feedback<br>Questions|/FrontOffice/<br>FeedBackForm|Question, Sequence,<br>Type (Rating /<br>Descriptive), Applicable<br>to<br>(Parent/Student/Both),<br>Form type, Feedback<br>type, User type|Categories:<br>Infrastructure,<br>Administration,<br>Academics, About<br>Teacher, Transport,<br>Hostel, Library, Mess,<br>Safety, Student<br>Success. Add Question,<br>Manage Form visibility|
|Feedback & Survey ›<br>Subject Wise<br>Questions|/FrontOffice/<br>GetSubjectWiseFeedBac<br>kFormQuestions|AY|Question list per<br>subject|
|Reports › Public|/Report/|Form,Consolidated/|Manage Public Survey|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Survey Forms|healthsurveyformreport|Detailed, Date|Forms, Get|
|Reports › General<br>Feedback Form|/FrontOffice/<br>FeedBackFormData|Br, Form, Student type,<br>Consolidated / Detailed,<br>Date|Get, Take Form|
|Reports › Subject<br>Wise Feedback|/FrontOffice/<br>SubjectWiseFeedBackFo<br>rmData|Br, Cls, Subject, Form,<br>Month, Format (Class /<br>Staff wise)|Get|
|Reports › Feedback<br>Form Status|/FrontOffice/<br>FeedBackFormDataCou<br>nts|Br, Cls, Form, Student<br>type, Cycle 1–5|Tabs: General Form,<br>Subject-wise Form|
|Reports › Survey<br>Forms|/FrontOffice/<br>SurveyFormData|Location, Br, Cls, Sec,<br>Status, Form, Type|Get|
|Reports › Public<br>Forms|/Organisation/<br>DynamicFormColumnsB<br>yFormType|Br, Form, DR, Payment<br>status (Paid / Not paid)|Get|
|Reports › Event<br>registrations|/Report/<br>RptPublicEventRegistra<br>tions|Dates|Show Report|
|Reports › Student<br>Default Forms|/FrontOffice/<br>ViewDefaultTransportco<br>ntinutionDynamicform|Br, Form (e.g. transport<br>continuation), DR|Get|



#### **Dynamic forms — every field (deep-dive)** 

Alpha has no custom Student, Staff or Public forms in any year from 2024-25 to 2027-28; every list returns "No data found". So the fields below are what the form builder offers, plus the three built-in system forms. 

#### **Form header fields (Student / Staff / Public builder)** 

|Field|Type / options|
|---|---|
|Form Name|Text ("Name Your Form")|
|Last date for filling (Parent Portal / Staff Login)|Date|
|Form access|Apply for all branches / Apply for selected|
|Branches, Boards, Classes, Sections|Multi-select (visibility scope)|
|IsDefault, IsActive|Checkbox|
|Reference URL|Text("Add URL for Reference")|



|Field|Type / options|
|---|---|
|Terms and Conditions|File upload|
|Online Form URL, Shorten URL|Generated link + bit.ly short link|
|Public only: Is form applicable to|Both (insider / outsider), Inside students, Outside<br>students|
|Public only: Form type|Data collection with / without online fee payment<br>(fee type + collection account)|
|Staff only: Copy from existing form|AY, Existing form, New name, Last date|



#### **Field types in the builder palette (17)** 

Text, TextArea, Integer, Percent, Phone, Email, DateTime, Time, Pick List, Multiselect Pick List, Radio Button, Radio Button (YES/NO), Radio Button (NO/YES), Checkbox, Label, PDF Upload, Image (student forms only), System Generated Number. 

**System (merge) fields available in student forms (~150)** — prefilled from the student record with the @ prefix: 

- Identity: Student Name, First/Middle/Last name, Gender, Pronoun, Date of Birth (figures, words, several formats), Place of Birth (village, state, country), Nationality, Religion, Caste, Sub Caste, New Sub Caste, Reservation Type, Mother Tongue, Blood Group, Identification marks 1–2, Photo (standard and 90×90), QR Code 

- IDs: Enrollment Code, Admission No, Unique ID, Aadhaar No, State Govt ID, Govt Unique ID, PEN Number, APAAR No, Smart Card No, Hall Ticket No, CSR Code, Certificate No, Challan No 

- Academic: Academic Year, Class, Section, Class Type, Class Group, Admitted Class, Present / Promoted class (in words), Previous Class, Previous School, Term name/period, Subject Details, Rank, II/III Language, Class Teacher name/sign, Course Duration, Year of admission, Admitted AY 

- Dates: Date of Admission (formats, words), Date of Application, Today (several formats), NOW, NOP 

- Family: Father/Mother name, phone, email, DOB, qualification, occupation, annual income, photo, Govt ID; Guardian name/phone; Sibling name & class; Emergency contact; Address, City, District, State, Country 

- Fee: Fee details, Fee-type fee details, Installment name, Installment-wise ledger, Due date, Duedate-wise balance, Late fee, Amount to be paid (with late fee), Amount in words, Fee paid / due amount, Tuition fee paid, Concession available / amount / fee type 

- Attendance & transport: Monthly attendance, Daily attendance, Bus route name 

- Organisation: Organisation name, Branch name, Branch address, Branch logo 

Staff forms offer the same 17 field types but no student merge fields. 

#### **Built-in system forms (student)** 

|Form|Endpoint|Fields|
|---|---|---|
|Correction<br>Form|/Organisation/<br>CreateStudentCorrectionForms|Same header + System Fields picker: parents<br>choose which student fields to correct|
|Registration<br>Form for Next<br>AY|/FrontOffice/<br>ExistingStudentContinutionDyna<br>micForm|"Registration for new session" + I Agreed, Yes /<br>No, Save|
|Transport<br>Continuation<br>Form|/FrontOffice/<br>TransportContinutionFormDyna<br>micForm|Read-only: Student name, GR No, Admission No,<br>Class, Section, Father name/mobile/email,<br>Mother name/mobile/email, Vehicle No, Current<br>pick-up point, Current drop point, Monthly /<br>annual transport fee plans. Choice: Continue with<br>same details / Continue but need changes / Opt<br>out. Save|



For Django: one <mark>DynamicForm</mark> (scope, type, dates, fee link) + <mark>DynamicField</mark> (type, label, options, required, order, merge_key) + <mark>DynamicResponse</mark> / <mark>DynamicAnswer</mark> will cover all three builders. 

### **Learner Profile** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Student Discipline ›<br>Discipline Observations|/AcademicPlanning/<br>DesplineDetailsReport|Br, AY, Form type<br>(Normal / Anti-<br>Bullying), DR|Get, Learner Profile<br>link|
|Student Discipline ›<br>Manage Discipline<br>Category|/AcademicPlanning/<br>CreateCodeofConduct|Category, Sub category,<br>Negative marks, Short<br>code, Form type,<br>Severity<br>(Minor/Moderate/Serio<br>us)|Add/Edit Category &<br>Sub category, View<br>Discipline Master.<br>Seed examples:<br>Shouting, Beating,<br>Foul language,<br>Answering back,<br>Damaging property…|
|Academic Observations<br>› Student Observations|/Connect/<br>LearnerProfile_New|Br, Grade|Record Observation|
|Student Anecdotes ›<br>Manage Anecdotes|/Report/AddAnecdotes|Type (Appreciation /<br>Needs work), Name,<br>Max badges/stars (5–<br>10), Icon (upload or<br>gallery), Update<br>portfolio,<br>Email/SMS/Appnotify|Create/Update. Cols:<br>Name, Type, Max<br>badges, Image,<br>Portfolio,<br>Notifications, Actions|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|||parent||
|Student Anecdotes ›<br>Anecdotes Report|/StudentMoments/<br>AnecdotesDetailsDashbo<br>ard_New|Br, Cls, Sec, Month|Get|
|Student Anecdotes ›<br>Learner Profile|/Connect/<br>LearningProAssessmentS<br>tudentResults|Br, Board, Cls, Sec|Get → learner profile<br>results|
|Achievements › Student<br>Achievements|/StudentMoments/<br>StudentSchoolAchievem<br>entsMonthwise|Br, Category, Sub<br>category, Competition<br>level, Month|Quick add (one<br>student, one<br>achievement). Tabs:<br>Participation, All<br>Events|
|Reports › Discipline<br>Summary Marks Count|/Report/<br>RptCOCStudentSummary<br>MarksCount|Br, Cls, Dates|Get|
|Reports › Discipline<br>Remarks|/Report/<br>DisciplineRemarks|Br, Cls, Dates|Get|
|Reports › Discipline<br>Marks By Staff|/Report/<br>RptCodeOfConductMark<br>sOfStudentByStaff|Br, Dates|Get|
|Reports › Discipline<br>Detailed Marks|/Report/<br>RptCocStudentDetailed<br>Marks|Br, Cls, Sec, Dates|Show Report|
|Reports › Discipline<br>Marks By Category|/Report/<br>RptCodeOfConductStude<br>ntSummaryByCategory|Br, Cls, Sec, Category,<br>Dates|Show Report|



### **Transport** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Route Management ›|/Transport/|Br|Views: Trips, Routes &|
|Manage Trips|Transport_New_EagleEY<br>E||Stops, Zones & Areas|
|Route Management ›|/Transport/|AY, Br|Tabs: Create Bus|
|Bus Routes|CreateBusRouteDetails_||Route, Upload Bus<br>Route,Upload Bus|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Management|New||Stop, Manage<br>Transport Staff,<br>Vehicle details, Special<br>Route Students. Assign<br>route to staff; copy<br>routes to next AY|
|Route Management ›<br>Month wise Transport<br>details|/Transport/<br>RptTransportMonthWis<br>eFeeReceReport|Br, Status|Tabs: Route wise<br>strength, Routes-Fee<br>plans, Routes-Classes,<br>Student-Routes-Fees,<br>View Fee Plans|
|Route Management ›<br>Assign Bus Routes to<br>Students|/Transport/<br>AssignBusRoutesToStud<br>ent_Main|Br, Route, Cls, Sec,<br>Pickup stop, Drop stop,<br>Fee plan, Pickup/Drop<br>route|Assign Stops and Fee<br>plan. Cols: Enrollment<br>Code, Student,<br>Admission No,<br>Address, Pickup/Drop<br>stop, Pick/Drop time,<br>Fee Plan|
|Route Management ›<br>Daily MIS- Transport<br>Incharge|/Report/<br>TransportInchargeDaily<br>Mis|Br, Month|Get|
|Route Management ›<br>Assign Vehicles to<br>Branches|/Organisation/<br>AssignBranchVechicle|Br|Get, All Branch Vehicle<br>Details report|
|Route Management ›<br>Vehicle Scanner|/Transport/<br>VehicleScanner|—|Cols: Vehicle No,<br>Branch, Routes,<br>Timings Error|
|Transport Fee ›<br>Transport Fee<br>Receivables|/Transport/<br>RptTransportFeeReceRe<br>port|AY, Br, Status|Tabs: Class-wise<br>receivable, Fee plan<br>class-wise, Vehicle<br>seating summary,<br>Route-Class, Route-<br>wise receivable, Paid &<br>Due, Siblings, Staff<br>availing transport,<br>Receivable report|
|Transport Fee › Bus<br>Route Wise Feeplans|/Transport/<br>RouteWiseFeeplans_Mai|Br, Route|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||n|||
|Transport Fee › Upload<br>Transport Fee<br>Receivables|/Transport/<br>UploadFeeReceivables|Br|Excel upload|
|Transport Fee › Assign<br>Transport Fee To<br>Student|/Transport/<br>AssignTransportFeeToSt<br>udent|Br, Class category, Cls,<br>Sec, Route; filter radio<br>(route & fee not<br>assigned / route only /<br>fee only)|Get Students, Assign<br>Fee to Selected. Tabs:<br>Fee with Route,<br>without Route, Fee<br>Assigned, Route & Fee<br>Assigned, Route-wise<br>Fee plans, Bulk,<br>Upload|
|VTS › GPS SMS Settings|/Organisation/<br>TransportGPSSMSSettin<br>gs_New|Per-branch toggles|Cols: Branch, GPS SMS,<br>GPS Notification,<br>Action|
|VTS › VTS Vendor URL<br>Track Settings|/Organisation/<br>BranchesWiseVTSVendo<br>rs|Br, Vendor, Username,<br>Password, Common<br>URL, Active|Add/Edit vendor|
|VTS › Dashboard|/Transport/<br>TransportNotificationDa<br>shBoard|Br; enable VTS for<br>parents (Y/N)|Live tracking + today's<br>notifications|
|VTS › Notifications|/Transport/<br>GetTransportNotificatio<br>nsdetails_MonthwiseGe<br>t|Br|Date-wise notifications|
|VTS › Refresh Vehicle<br>Details|/Transport/<br>VTSRefreshAPI|Br|Pull vehicles from VTS<br>vendor API|
|Transport Attendance ›<br>Month Wise Detailed|/Connect/<br>StudentTransportAttend<br>ance_MonthWise|Br, Route, Cls, Sec,<br>Pickup / Drop|Get|
|Transport Attendance ›<br>Monthly|/Transport/<br>StudentTransportAttend<br>ance|Br, Route, Month|Present / Absent<br>counts|
|Route Intelligence ›<br>Manage Transport<br>Zones|/Organisation/<br>ManageTransportZones|Br|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Route Intelligence ›<br>Nearest Locality|/Transport/<br>RptStudentNearestLocal<br>ity|Br, Cls|Get|
|Route Intelligence ›<br>Zone-wise Students|/Organisation/<br>ZoneWiseStudentsMap|Br, Zone|Map|
|Route Intelligence ›<br>Student Address<br>Google Map|/Transport/<br>RptSectionwiseTranspor<br>tMap|Br, Cls, Student type,<br>address autocomplete|Tabs: Google Map,<br>Locality wise, Distance<br>wise|
|Reports › Student Bus<br>Attendance Daywise|/Student/<br>StudentBusAttendance|Br, Route, Date|Get|
|Reports › Vehicle Fuel<br>details|/Transport/<br>VehicleFuelDetailsRpt|Br, Vehicle, Month /<br>Date wise|Get|
|Reports › Vehicle Data<br>Collection|/Transport/<br>GetTransportVehicleDat<br>aCollectionReport|Br|Show|
|Reports › Transport<br>Month wise|/Transport/<br>RptTransportMonthsWis<br>eReports_Main|Br, Status|Tabs: Route, Slab,<br>Route+Slab, Class (fee<br>payable), Class type|
|Reports › Drivers and<br>Cleaners|/Transport/<br>GetBusDriverDetails|AY, Br|Get|
|Reports › Route and<br>Month Wise Fee|/Transport/<br>TransportMonthWiseStr<br>ength_FeeTypesandSlab|Br, Installment, Student<br>status|Show Report|
|Reports › Monthwise<br>Transport Details|/Transport/<br>TransportRouteWiseStu<br>dentDetails_Main|Br, Class-Sec, Route, Till<br>month / Custom,<br>Month, Status, Show<br>fee|Tabs: Route wise, By<br>pickup time, By drop<br>time, Consolidated|
|Reports › Other<br>Reports|/Report/<br>TransportWiseandClass<br>WiseStudentList|Br, Class / Transport<br>wise, Data type<br>(Students, Attendance,<br>Transport fee, Class<br>group, House),<br>Present/Absent, Route,<br>Cls, Sec|Get|
|Reports › Bus wise<br>Expenses|/Transport/<br>BusWiseExpensesDetails|Br, Vehicle, Type<br>(Breakdowns/Fuel/Mai|Get|



|Group › Page|Endpoint|Filters / inputs|Actio|ins, tabs, columns|
|---|---|---|---|---|
||_Transport|ntenance), 6 months /<br>DR|||
|Reports › Daily MIS-<br>Transport|/Report/<br>RptTransportIncharge_<br>MIS|Br, Month / Date wise,<br>Pickup / Drop|Get||
|Reports › Vehicle<br>Mileage|/Transport/<br>VehicleMillageDetailsRp<br>t|Br, Vehicle, Month /<br>Date wise|Get||
|Reports › Vehicle<br>Seating Capacity|/Transport/<br>GetVehicleSeatingCapaci<br>ty|Br, AY|Show|Report|
|Reports › Consolidated<br>Transport|/Transport/<br>ConsolidatedTransportR<br>eport|AY, Br, Cls, Sec, Status|Get||
|**Login Statistics**<br>Group › Page|Endpoint|Filters / inputs||Actions, tabs,<br>columns|
|Login Settings ›<br>Student/Parent 2 Step<br>Auth|/Organisation/<br>GetSecondLevelAuthen<br>ticationSettings|Radio: Email OTP, MPIN, N<br>OTP, Gmail auth, Microsoft<br>auth; OTP in mobile app|o<br>t|Change|
|Login Settings ›<br>Admin/Staff 2 Step<br>Auth|/Organisation/<br>GetSecondLevelAuthen<br>ticationSettings_Admin<br>s|Radio: Email OTP, 4-digit<br>MPIN, Gmail, Microsoft||Change|
|Password Help ›<br>Password Settings|/Organisation/<br>PasswordSettings|Password format for<br>Student/Parent (Enrollmen<br>code) and Staff (Staff code)|t<br>f f|Tabs:<br>Organisation,<br>Zonal, Branch,<br>Staff|
|Password Help › Set<br>Alias UserName|/Student/<br>ResetAliasUsername|Student/Parent or Staff, Br<br>Cls, Sec, Login type; alias =<br>Admission No / Mobile /<br>Admission No+First name|f ,<br>|Get Students,<br>Set / Reset Alias|
|Password Help › Reset<br>Passwords|/Student/<br>ResetPassword|Same filters; password = D<br>(2 formats) / Custom / Fath<br>mobile|i   OB<br>er|Reset Password.<br>Cols: Enrollment<br>Code, Admission<br>No,Name,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||||Father<br>name/email,<br>Username, Alias,<br>DOB, Father<br>mobile, Cls, Sec|
|Password Help ›<br>Change Password<br>Statistics|/Student/<br>Changepasswordstatisti<br>csCount|Br, User type<br>(Parent/Student/Staff), AY,<br>Consolidated / Detailed|Get|
|Password Help ›<br>Student/Parent Login<br>Details|/Report/<br>LoginDetails_student_p<br>arentDetails|Br, Cls, Sec (active only)|Get; click<br>username to<br>resolve login<br>issues|
|Reports › Users Not<br>Loggedin|/Report/<br>UserNeverLoginsRpt|Web / App, Never / 7 / 30<br>days, User type, Br|Show Report|
|Reports › Logins log|/Report/<br>PopulateUsersLog|AY, Br|Mobile apps<br>usage|
|Reports › User Login<br>Analysis|/Report/<br>Userloginanalysis|Location, Br, DR (up to 6<br>months)|Show|
|Reports › User Login<br>details|/Report/<br>PopulateAdminUserLog<br>inDetails|AY, User type<br>(Admin/Staff/Student/Parent),<br>Br, Dates, Logged in / Not|Get|
|Reports › Login access<br>disabled|/Student/<br>StudentUsersInActive|Br, Cls, Sec|Manage Parent<br>Portal Access,<br>Get|
|Reports › Sibling<br>Account in parent app|/Report/<br>SiblingAccountinparent<br>mobileapp|Br|Get|



### **Certificates** 

Certificate pages share one student-search form: search by Student Name / Application No / Enrollment Code / Admission No / GR No, status (Active / Inactive / Alumni / Transfer Out). The student panel shows DOB, blood group, category, father/mother name-mobile-email and current address, editable before printing. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Settings › Certificate<br>No. Generation|/Connect/<br>CertificateGenerationSe<br>ttings|Br, Certificate type|Numbering series per<br>type|
|General › Student<br>Certificate Design|/Certificates/<br>CertificateDesign_New|—|Tabs: Bonafide &<br>Study, Income Tax,<br>DOB & Conduct,<br>Deposit, Others, No<br>Due, Promotion|
|General › Student<br>Certificates|/Report/<br>PopulateCertificatesTake<br>n|Br, Type, AY, Last 6<br>months / custom dates|Tabs: Consolidated,<br>Detailed; links to<br>generate Promotion /<br>Other / No Due|
|General › Staff<br>Certificates|/Staff/<br>PopulateStaffCertificates|Br, Type, dates|Issue Certificate,<br>Certificate Designer|
|General › Generate<br>Bonafide and Study|/Connect/<br>BulkGenerateCerificate_L<br>atest|Br, Cls, Sec, Status|Get → bulk generate|
|General › Generate<br>Other Certificate|/Organisation/<br>Search_IssueCertificate_I<br>ndex|Br, Class-Sec, Type,<br>Status, Search by, AY +<br>student edit panel|Search, Update. Tabs:<br>Issue TC, Fee Due<br>Details|
|General › Generate<br>Promotion Certificate|/Certificates/<br>GeneratePromotionCerti<br>ficate|Br, Cls, Sec, Students,<br>Certificate|Get, Print|
|General › Generate<br>No Fee due Certificate|/Organisation/<br>Search_NoDueCertificate|Br, Class-Sec, AY, Status,<br>Search by|Search, Update|
|ID Cards › ID Card<br>Design|/Certificates/<br>StudentIDCardsDesign_M<br>ain|Location, Br, Type<br>(Student/Staff/General),<br>Design|Tabs: Student, Staff,<br>APAAR ID card<br>designs|
|ID Cards › Print<br>Student ID Cards|/Certificates/<br>StudentIDCardsPrinting|Br, Class-Sec, House,<br>Admission type<br>(Old/New), Student type<br>(Day / Residential /<br>Semi), Transport,<br>Design, Students, Sort|Get → print|
|ID Cards › Print Staff|/Certificates/|Br, Department<br>(Teaching /Non-|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|ID Cards|StaffIDCardsForPrint|teaching / Transport /<br>Outsource…), Design,<br>Staff, Status||
|ID Cards › Generate<br>Bar Code|/Certificates/<br>StudentBarCodes|Br, Class & Section|Student barcode<br>generation|
|ID Cards › Bulk<br>Generate APAAR ID<br>Cards|/Certificates/<br>APAARIDCard_BulkDataB<br>ySections|Br, Programme<br>category, Course, Cls,<br>Sec, Transport,<br>Category, Design,<br>Admission type,<br>Students, cards per row,<br>rows per page, spacing,<br>display/format,<br>width/height px|Print|
|TC › Transfer<br>Certificate Design|/Certificates/<br>CertificateDesign_NewPa<br>rtial|— (redirects to MCB<br>error page)|TC template designer|
|TC › Generate<br>Transfer Certificate|/Organisation/<br>Search_IssueCertificate_I<br>ndex|Same student search|Tabs: Issue TC, Fee<br>Due Details|
|TC › Bulk TC<br>Generation|/Connect/<br>BulkTCGenerateCerificate<br>_Latest|AY, Br, Cls, Sec|Issue TC by<br>checkpoint|
|Achievements ›<br>Certificate Design|/Certificates/<br>ActivityCertificateDesign_<br>New|—|Tabs: Competitions,<br>Academic Excellence,<br>Awards, Anecdotes,<br>ECA, Olympiads, Staff<br>Achievement|
|Achievements › Issue<br>Certificates|/Certificates/<br>ActivityIssueCertificate_N<br>ew|Br, AY, DR|Tabs: Competitions,<br>Academic Excellence,<br>Awards, Olympiads;<br>Add Student<br>Achievements|
|Bonafide Letters ›<br>Design|/Certificates/<br>CertificateDesign_NewPa<br>rtial|Certificate name|Browse MCB<br>templates, Create<br>new design|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Bonafide Letters ›<br>Bonafide Letters|/Connect/<br>GetSchoolBonafide_Lette<br>rs|Br|List|
|Reports › Bulk<br>Student ID Cards|/Certificates/<br>StudentIDCard_BulkData<br>BySections|As APAAR bulk + House<br>group|Print|
|Reports › Bulk Staff ID<br>Cards|/Certificates/<br>StaffIDCard_BulkDataByS<br>ections|Br, Department, Design,<br>Status, layout|Print|
|Reports › Certificate<br>taken students|/Report/<br>PopulateCertificatesTake<br>n|Br, Type, AY, dates|Consolidated,<br>Detailed|



### **Library** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Digital Library › Digital<br>Library|/Library/<br>RptGetAllEbookLearnin<br>gLibraryBooks|Class, Subject, search|Add digital book,<br>NCERT textbooks,<br>Upload, Bulk assign.<br>Cols: Book Name,<br>Genre, Ref Code,<br>Language, URL/Path,<br>Assigned Classes,<br>Action|
|Settings › Create<br>Library|/Library/LibraryCreation|Br, Library name, Default<br>student search, Default<br>book search (Access No /<br>Title / ISBN), Active|Add Library, Add<br>Librarian, Central<br>Library. Cols: Branch,<br>Library, Librarian|
|Settings › Library<br>Categories|/Library/<br>LibraryCategoryName|Category, Sub category,<br>assign classes|Enable specimen<br>copies. Seeds: English,<br>Fiction, Non-Fiction|
|Settings › Library<br>Publishers|/Library/<br>LibraryPublishers|Name, Excel upload|Cols: Publisher,<br>Category|
|Settings › Library<br>Category Type|/Library/<br>LibraryCategoryType|—|Cols: Category Type,<br>Short Code|
|Settings › Library|/Library/LibraryVendors|Name, upload|Add Vendor|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Vendors||||
|Settings › Library<br>Languages|/Library/<br>LibraryLanguages|Language|Add|
|Settings › Create<br>Maximum Books|/Library/<br>CreateMaximumBooks|—|No. of books allowed<br>per user type|
|Settings › Library Fine<br>Amounts|/Library/<br>CreateLibraryFineAmou<br>nts_New|Late fine per day,<br>Damage fine (% of cost),<br>Lost fine (% of cost)|Per branch, Edit|
|Settings › Generate<br>Book Barcodes|/Library/<br>GenerateLibrary_Barco<br>des|Library, Br, Category<br>type/name, Language,<br>Access No / ISBN, All /<br>selected, Format 1–5,<br>Dimension, Copies|Generate|
|Settings › Book Return<br>Days|/Organisation/<br>LibraryBookReturnDays<br>Settings|Days for Student, Staff<br>per branch (e.g. 7 / 15)|Edit|
|Assessment › Grade<br>Wise Lexile Ranges|/Library/<br>ClasswiseLexilelevelRan<br>ges|Branch type, Board|Get|
|Assessment › Lexile<br>Grading Scale|/Library/<br>CreateLexileGradingScal<br>e|—|Cols: Scale, Grade,<br>Grade point, Remarks,<br>Icon|
|Assessment › Groups<br>and Parameters|/Connect/<br>GetLibraryAssessmentG<br>roups|Board, Class|Get|
|Assessment › Student<br>Reader Ability|/Connect/<br>StudentLibraryAssessm<br>entParameterResults|Br, Cls, Sec|Tabs: Term I, II, III,<br>Consolidated|
|Reports › Books wise<br>issue|/Communication/<br>LibraryBooksIssueWiseR<br>pt|Library, Br, Dates|Cols: Category type,<br>Category, Title, Access<br>No, Count|
|Reports › Student<br>wise Issued / Return|/Library/<br>StudentBooksIssuedDat<br>a_Rpt|Library, Br, Cls, Dates|Cols: Student,<br>Admission No,<br>Category, Language,<br>Access No, Title,<br>Status,Reserve date,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||||Return date|
|Reports › Library Book<br>Details|/Library/<br>LibraryBookBasicDetails<br>_Main|Library, Br, Category,<br>Status, Language,<br>Purchased / Entry date|Tabs: Book details,<br>Category wise, Book-<br>wise count|
|Reports › Usage Log|/Library/<br>LibraryUsageLog_Main|Library, Br, 3 / 6<br>months / custom, User<br>log / Class log|Get|
|Reports › Issue /<br>Return|/Library/<br>RptBookIssueOrReturn|Library, Br, Dates, Filter<br>by (Issue / Due / Return<br>date), Issue type, User<br>type, Cls|Get|
|Reports › Library Dash<br>Board|/Library/<br>LibraryDashBoard_New|Library|Dashboard|
|Reports › Staff Prof.<br>development Log|/Library/<br>GetLibraryBookdetails_<br>Report|Library, Br, Type (Book<br>reading / Online research<br>/ Workshops…), Dates|Get|
|Reports › Students<br>Library Fine|/Library/<br>StudentsLibraryFineRpt|AY, Library, Br, Cls, Sec,<br>Paid status|Tabs: Late fee,<br>Damage, Lost,<br>Consolidated|
|Reports › Library Book<br>Index|/Library/<br>LibraryBookIndex|Library (one per school),<br>Search by Title / Author|Get|



### **Hostel** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Building › Building<br>Details|/Hostel/<br>HostelBuildingDetails_M<br>odified|Building, No. of floors|Add/Edit building,<br>Add/Edit floors<br>(rooms, beds)|
|Building › Map<br>Buildings To Branches|/Hostel/<br>HostelMapBuildingsToBr<br>anches|Building|Assign. Cols:<br>Branches, Building|
|Management › Fee<br>Deposit Categories|/Finance/<br>GeneralCreateCategory|Category, Transaction<br>type (Dhobi / Medical /<br>Misc / Others), Fixed min<br>deposit, Collection|Tabs: Hostel<br>Deposits,<br>Collection<br>Accounts|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|||account||
|Management › Fee<br>Collection Day Sheet|/Hostel/<br>RptHostelFeeDaySheet_<br>New|Hostel, Br, Fee account,<br>DR, Payment mode,<br>Transaction type, Receipt<br>date type, Individual /<br>Consolidated, PDC|Show Report|
|Management › Hostel<br>Leave Types|/Hostel/<br>GetHostelLeaveTypes|—|List|
|Management ›<br>Attendance Remarks|/Hostel/<br>HostelAttendanceRemar<br>ks|Absent reason|Add/Edit|
|Management › Create<br>Category & Items|/Hostel/<br>HostelCreateCategory|Category, Description,<br>Type, Item, UOM|Upload items.<br>Tabs: Provisions,<br>Fruits &<br>Vegetables,<br>Housekeeping, Gas<br>& Fuel, Electrical|
|Management ›<br>Attendance|/Hostel/<br>HostelAttendance|Hostel, By Class / Floor,<br>Floor, Room, Date|Get, Upload<br>absentees, Leave<br>application|
|Management › Apply<br>leave for Hostlers|/Hostel/<br>CreateHostelLeave|Br, Class, student search,<br>Leave type, From–To,<br>Remarks|Save|
|Management › Daily<br>Purchases /<br>Consumables|/Hostel/<br>HostelPurchaesandExpe<br>nses|Building, Category, Item,<br>DR|Tabs: Daily<br>Purchases, Daily<br>Consumables,<br>Hostel Vendors|
|Management › Create<br>Announcements|/Hostel/<br>CreateHostelAnnounce<br>ment|Br, Type, Title, Display<br>type, Dates, Scroll on<br>homepage, Buildings,<br>Student/Parent,<br>Class/Section wise,<br>Description, Attachments<br>(30MB)|Save|
|Management › Student<br>Items to be Brought|/Hostel/<br>HostelStudentItemsTOB|AY|Manage Category<br>Items|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||eBrought|||
|Management ›<br>Admission|/Hostel/<br>CreateHostelAdmission|Hostel, Br, AY, Class-Sec,<br>Category (Residential /<br>Semi / AC), Gender|Get → allot bed|
|Management › Warden<br>Remarks|/Hostel/<br>GetHostelStudentWarde<br>nRemarks|Br, Cls, Floor, Date|Get|
|Meals › Meals Settings|/Hostel/<br>ManageHostelSettings|—|Tabs: Meal<br>category items,<br>Seasons, Meals|
|Meals › Daily Meals<br>Menu|/Hostel/<br>HostelDailyMealsMenu|Location, Category,<br>Season, Item, Weekday,<br>Meal, Branches|Tabs: View, Assign.<br>Cols: Branch, Item,<br>Week days, Meals|
|Meals › Schedule Meals|/Hostel/HostelSchedule|Category, Items, Location,<br>Season, From–To time,<br>Branches|Tabs: Add, Existing|
|Others › Warden<br>Details|/Hostel/<br>HostelWardenDetails|Br, Hostel, Warden|Tabs: Existing,<br>Assign. Cols:<br>Name, Address,<br>Contact|
|Others › Committee<br>Entry Form|/Hostel/<br>CommityEntryForm|Committee, Head, Date,<br>Members, Task|Create|
|Others › Committee<br>Members Entry|/Hostel/<br>CommityMembersEnter<br>yForm|Committee, Head, Date,<br>Task|Get|
|Reports › Building<br>Details|/Report/<br>HostelBuildingDetailsRe<br>port|—|Cols: Floor, Room,<br>Bed, Student,<br>Class, Section,<br>Branch|
|Reports › Mess Menu|/Report/<br>RptHostelMessMenu|Location, Br, Season|Get|
|Reports › Item<br>Transaction Details|/Hostel/<br>RptHostelItemTransType<br>Details|Br, Category, Item, DR|Get|
|Reports › Mess Report|/Inventory/|Location,Br,Category,|Show|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||GetHostelDailyPurchase<br>sReport|Dates||
|Reports › Category<br>Deposits / Transactions|/Report/<br>RptForHostelCanteenTra<br>nsactions|Br, Deposit category,<br>Status, FY, DR|Get|
|Reports › Schedule<br>Report|/Report/<br>HostelScheduleReport|Location, Br, Category,<br>Season|Get|
|Reports › Committee<br>Head Report|/Hostel/<br>CommitteeHeadReport|Committee, dates|Update task. Cols:<br>Committee, Head,<br>Member, Task,<br>Accomplished,<br>Status, Concern,<br>Next-week plan|
|Reports › Gate Pass<br>Permission|/Report/<br>RptGatePassPermissions|Location, Br, Dates,<br>Student / Staff wise|Get|
|Reports › Food Items|/Report/RptFoodItems|Location, Br, Category,<br>Dates|Get|
|Reports › Hostel<br>Attendance|/Hostel/<br>HostelAttendanceReport|Br, Hostel, Month|Get|
|Reports › Bed<br>Allotment|/Report/<br>HostelReportForBedAllo<br>tment|Location, Br, Hostel, User<br>type (Student / Guest),<br>name/phone/code|Cols: Name,<br>Enrollment, Floor,<br>Room, Bed,<br>Admission No,<br>Date, Admitted by|
|Reports › Warden<br>Details|/Login/ErrorHandler|—|Broken in MCB<br>("Oops something<br>went wrong")|
|Reports › Leave Details|/Hostel/<br>RptHostelLeaveForStude<br>nt|Br, Dates|Get|
|Reports › Student Wise<br>Transactions|/Report/<br>RptForHostelStudentCan<br>teenTransactions|Br, Deposit category,<br>Status, FY, DR|Get|
|Reports › Vendor Wise<br>Purchases|/Hostel/<br>Hostel_VendorWisePurc|Br, Dates, Category,<br>Vendor|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||hases|||



### **Concerns (helpdesk / tickets)** 

Concern types carry: category, type, description, notice period, escalation days to L2 and L3, response and resolution target hours, "users can raise indent" flag, and responsible person at organisation and branch level. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Concerns ›<br>Dashboard|/ServiceRequest/<br>ConcernsDashBoard_Main|AY, Location, Br, Period (7 /<br>30 / 90 days / AY to date)|Get|
|Concerns › Search<br>Concerns|/ServiceRequest/<br>ServiceRequestTicketSearc<br>h|Reference No|Cols: Ref No,<br>Type, Message,<br>Booked by, Date,<br>Status; View<br>history|
|Concerns › Map<br>Users to Class<br>Categories|/Organisation/<br>MaporganizationUserstoCl<br>assCategories|Location, Br, User type<br>(Organisation / Zonal)|Get|
|Staff › Staff Concern<br>Types|/Menu/<br>ServiceRequests_New_Get|Type form (above);<br>categories Expenses claims,<br>Petty cash advance, Others|Add/Edit type,<br>sub concern, org-<br>level user, log|
|Staff › Update Staff<br>Concerns|/ServiceRequest/<br>ViewStaffConcern_Principa<br>l|AY, Br, Status, Department,<br>DR|Get|
|Parent › Parent<br>Concern Types|/Menu/<br>ServiceRequests_New_Get|Categories Academic, Non-<br>Academic, Transport,<br>General, Complaints,<br>Feedback, Fee, Promotion,<br>Appointments, Health…;<br>request types (transport,<br>rejoin, cancel, change<br>route…)|Same type form|
|Parent › Parent<br>Service Requests|/ServiceRequest/<br>ViewStudentRequestCateg<br>oryDetails|Org-level user (name, email,<br>mobile, type)|Cols: Category,<br>Type, Responsible<br>person|
|Parent › Update|/ServiceRequest/|AY,Location,Br,Category,|Get,Settings|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Parent Concerns|Viewparentconcerns_Admi<br>nLevel|Status, DR||
|Parent › Responsible<br>Person|/ServiceRequest/<br>ViewParentConcernSetting<br>s|Handling type 1–4 with<br>Levels 1–3|Matrix: category<br>× branch<br>responsible<br>person|
|Branch › Branch<br>Concern Types|/Menu/<br>ServiceRequests_New_Get|Inter-office types|Same type form|
|Branch › Update<br>Branch Concerns|/ServiceRequest/<br>ViewOthersConcern|AY, Br, Status, DR|Get|
|TC Requests ›<br>Dashboard|/ServiceRequest/<br>TCRequestDashboard|AY, Location, Br, Period|Get|
|TC Requests › Fee<br>Settings|/Finance/<br>MiscFeeTypesForTCReques<br>tFee|Fee type, Description, Is<br>processing fee, Is notice<br>period fee, Notice days,<br>Active|Add/Update|
|TC Requests ›<br>Configure|/Menu/<br>ConfigureTCRequests|Br|Workflow: parent<br>raises → class<br>teacher counsels<br>→ coordinator →<br>principal. Tabs:<br>Configure, Class<br>Coordinators,<br>Consolidated,<br>Detailed|
|TC Requests ›<br>Branch TC Request<br>Dates|/Organisation/<br>TCRequestBranchWise|Br|Request window<br>dates|
|Reports › Parent<br>Concerns Analysis|/ServiceRequest/<br>ParentConcernReport_Ne<br>w|AY, Location, Br, Detailed /<br>Consolidated, Category,<br>Type, DR|Get|
|Reports › Aging<br>Report|/Menu/<br>ConcernAgingSettings_Chil<br>d|Br, No. of days|Tabs: Aging<br>Settings, Report|
|Reports › Overall|/Report/<br>ConcernClassCategoryWise|Type (class category /<br>concern category /section/|Report|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Summary|Report|branch wise)||
|Reports › TC Request|/Student/|—|Consolidated,|
|Report|ConfigureTCRequest_Repo<br>rt||Detailed|



### **Achievements and Mentors** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Achievements ›<br>Institute<br>Achievements|/Organisation/<br>SchoolSpecificAchieve<br>ments|Filter: Br, AY, DR. Form: Branch,<br>Category, Sub category, Event<br>name, Description, From–To date,<br>Venue, City, Achievement|Add, Show<br>Report|
|Achievements ›<br>Student<br>Achievements|/StudentMoments/<br>StudentSchoolAchieve<br>mentsMonthwise|Br, Category, Sub category, Level,<br>Month|Quick add;<br>Participation /<br>All events|
|Achievements ›<br>Staff Achievements|/Student/<br>StaffSchoolSpecificAchi<br>evements|Filter: Br, AY, DR. Form: Category,<br>Sub category, Name, Description,<br>No. of days, Date, Venue, City,<br>Staff type, Staff, Achievement|Cols: Staff type,<br>Staff,<br>Achievement,<br>Action|
|Reports › Student<br>Achievements<br>Report|/Student/<br>Studentwiseachieveme<br>ntsReport|Br, AY, Cls, Sec, DR|Get|
|Mentors › Mentor<br>Wise Student<br>Details|/FeeCommon/<br>StudentDetailsMentor<br>Wise|AY, Br, Programme category|Get|



### **Finance (fees)** 

Core fee model: Fee Account (collection entity) › Fee Type (Regular / Misc / Transport / Application / Exam) › Fee Plan per class › Installments (one-time, installment, monthly) › assigned to students, with concessions, fines, scholarships, refunds and invoices. Payment modes include cash, cheque/DD, card, online PG; cheques go through deposit, clearance and bounce flows. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Fee Mgmt › Fee|/FeeManagment/|AY, Br, Classes|Tabs: Fee Plan wise,|
|Receivables Report|RptFeeReceviablesReport||Fee Type wise, Plan vs<br>Type,Installment wise,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||||Fee Account wise,<br>Invoice Register/Dues,<br>Receivables by<br>installment, Compare<br>Fee Plans, Section-wise<br>average fee|
|Fee Mgmt › Manage<br>Fee Invoice/Challan|/FeeManagment/<br>FeeInvoice_History|AY, Br, Cls, Sec, Invoice<br>term, Invoice / Challan|Generate invoices /<br>challans. Tabs: Batch-<br>wise, Invoice Registers,<br>Consolidated, Pre-<br>admission invoice,<br>Receipts, Cancelled,<br>Fine charges, Credits &<br>Discounts, Upload<br>invoice payments, Paid<br>& Due, Consolidated<br>paid, Fee-type-wise|
|Fee Mgmt › Bank<br>Reconciliation|/FeeManagment/<br>ViewReconciliation_Dash<br>board|Br, FY, Collection<br>account|Tabs: Cash Accounts,<br>Bank Accounts|
|Fee Mgmt › Bank<br>Reconciliation<br>Clearance|/FeeManagment/<br>BankClearanceCheque|Br, FY|Clear cheques, View<br>clearance, Upload<br>clearance cheques|
|Fee Mgmt › Assign<br>Fee to Students|/FeeManagment/<br>AssignFeeTo_Student|AY, Br, Cls, Sec, Regular<br>fee type, Segment,<br>Category, New/Existing,<br>Gender|Get Students. Assign<br>On-Demand (prepaid) /<br>Lunch / Enrichment /<br>Transport / Contract<br>fee plan. Tabs:<br>Summary, Assigned,<br>Not assigned, Upload<br>receivables, View Fee<br>Plans|
|Fee Mgmt › Misc.<br>Fee Assign/Unassign|/FeeManagment/<br>BulkAssignMiscFeeToStu<br>dents|Br, Misc fee type (Exam<br>fee, After-school, Day<br>care…), Cls, Sec, Gender,<br>Status|Tabs: Assign, Manage,<br>Upload receivables,<br>Upload concession,<br>Entity to classes,<br>Unassigned log,<br>Amount modified log,<br>Receipts|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Fee Mgmt › Fine<br>Management|/FeeManagment/<br>FineAmountManagemen<br>t|AY, Br, Fee type,<br>Installment|Tabs: View fine<br>settings, Student-wise<br>fine edit/delete, Fine<br>collection report,<br>Create fine settings|
|Fee Mgmt › Fee<br>Mismatch Details|/FeeManagment/<br>StudentFeeMismatchDet<br>ails|AY, Mismatch type<br>(Concession /<br>Receivables / Receipts)|Get|
|Fee Mgmt › Cheque<br>Deposit Dashboard|/FeeManagment/<br>RptChequeDepositeDetai<br>ls|Bank account, Br,<br>Transaction DR, Deposit<br>DR|Get|
|Fee Mgmt › GST<br>Settings|/FeeManagment/<br>CommonGSTSettings|FY, Br|Tabs: Fee-type tax<br>settings, SAC codes, Tax<br>settings|
|Fee Mgmt ›<br>Enrichment<br>Program|/FeeManagment/<br>BranchFeeCollectionRefu<br>nds|Br, Fee type. Form:<br>name, fee account,<br>refundable, online<br>payment, start–end<br>date, amount, event<br>description|Add collection type<br>(picnics, field trips)|
|Fee Mgmt › Bulk<br>Installment<br>Assign/Unassign|/FeeManagment/<br>FeeManagementTabs|AY, Br, Cls, Sec, Regular<br>fee type|Tabs: Assign summary,<br>Assigned students,<br>Assign installment,<br>Unassign installment,<br>Change Fee Plan|
|Fee Mgmt › Month<br>wise Bulk fee<br>unassign|/FeeManagment/<br>FeeManagementUnassig<br>n_New|AY, Br, Classes, Sections,<br>Service-based fee type,<br>Month|Get|
|Fee Mgmt ›<br>Unassign Misc Fee<br>(Bulk)|/FeeManagment/<br>BulkUnAssignMiscFeeToS<br>tudents|Br, Class, Misc fee type|Get|
|Fee Mgmt › Manage<br>Last year Dues|/FeeManagment/<br>FeeTypeMappedtoMiscF<br>ee|Br, From AY, To AY, Misc<br>fee type, Cls, Sec, Status,<br>Report type|Tabs: Map fee types,<br>Map entities, Upload LY<br>dues, Upload LY<br>concessions, Dues<br>dashboard, Previous<br>year dues,Processing,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||||LY dues receipts|
|Fee Mgmt › Fees for<br>Shuffled-out<br>students|/FeeManagment/<br>RptBranchShuffleOutStud<br>ents|Br, AY|Get|
|Approvals › Approve<br>Concession<br>Requests|/Finance/<br>ApproveConcessionRequ<br>estsStatusIndex_New|AY, Location|Get → approve/reject|
|Approvals › Approve<br>UnAssign Fee<br>Requests|/Finance/<br>ApproveFeeUnassignReq<br>uest_Main|AY, Location|Tabs: Request<br>dashboard, Finance<br>overview|
|Approvals › Fee<br>Payment Change<br>Requests|/Finance/<br>FeePaymentChangeRequ<br>estsStatusIndex_Main|AY, Location, Type<br>(Amount / Date /<br>Receipt change / Cancel)|Get|
|Approvals › Update<br>Fee Payment details|/Finance/<br>EditPaymentDetails|Br, Search by, Fee type<br>(Regular / Store /<br>Advance), AY, student|Search → edit receipt|
|Approvals › Approve<br>Student Fee<br>Refunds|/Finance/<br>ApproveStudentFeeRefu<br>nds|AY, Br; pay form: Paying<br>account, Amount, Type<br>(Cheque/DD / Online),<br>Cheque no, Txn ID,<br>Refund date|2-step approval<br>(Principal →<br>SysAdmin/Accounts).<br>Tabs: To be paid,<br>Processed, Pending,<br>Rejected, Fee-type<br>wise, Security deposit<br>refunds|
|Approvals › Update<br>Online Payment<br>details|/Finance/<br>OnlinePaymentsAdjustm<br>ent|Br, Search by (incl.<br>Transaction ID), Fee type|Search → adjust|
|Approvals › Edit<br>Application Details|/FrontOffice/<br>ApplicationFormDetails_<br>Edit|AY, Br, Search by<br>(name / enrollment /<br>application / father<br>mobile / txn)|Search → edit|
|Approvals › Edit<br>Registration Details|/Student/<br>RegistrationFormDetails_<br>Edit|Same|Search → edit|
|Approvals › Online<br>Payment Force|/Finance/<br>OnlinePaymentSearchInd|AY, Transaction ID|Search → mark success|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Success|ex|||
|Approvals › Delete<br>Fee Payments|/Finance/FeePayments|Br, Fee account,<br>Payment mode, AY,<br>Search (Enrollment /<br>Receipt date), DR|Search → delete|
|Approvals › Adjust<br>payments to Other<br>Student|/Finance/<br>StudentPaymentsAdjust<br>ment|Br, Offline / Online,<br>Search by|Search → move<br>payment|
|Approvals › Student<br>Credit Note Wallet|/Followup/<br>StudentCreditAmounts_<br>Main|AY, Br, Classes, Account|Tabs: Pending,<br>Approved, Upload<br>credit notes|
|Concessions ›<br>Manage Fee<br>Concessions|/Finance/<br>AssignConcessionsToStud<br>ents|AY, Br, Segment, Cls,<br>Sec, Regular fee type|Tabs: All students, Staff<br>kids, Sibling, Upload<br>fee-type wise, Upload<br>installment wise,<br>Manual installment|
|Concessions › Fee<br>Concessions Reports|/Finance/<br>FeeConcessionDetailsInd<br>ex|AY, Br, Status, DR,<br>Approval status, Class|Tabs: Fee type, Grade,<br>Fee type+installment,<br>By dates, By status,<br>Student list, Early-bird|
|Concessions › Staff<br>kids Concession|/FeeCollectionReports/<br>StaffKidsReport|AY, Br, Staff|Map staff to student|
|Concessions ›<br>Sibling Concession|/Transport/<br>RptSibilingReport|Br, Fee type, Gender,<br>Category, Transport|Show, Format 2|
|Collection › Fee Day<br>sheet|/FeeCollectionReports/<br>FeeDaySheetPartial_Mai<br>n|Report picker (Day<br>sheet, with GST, Fee-<br>type, Installment,<br>Payment mode…)|Report|
|Collection › Fee<br>Collection Reports|/FeeCollectionReports/<br>RptFeeCollectionReport|FY, Br, Fee account, DR<br>(to 90 days), Cancelled<br>logic, Payment mode,<br>AY, Format|Tabs: Receipts, Fee-<br>type receipts, With<br>GST, Online PG,<br>Advances, Other<br>collections, Cancelled,<br>Month-wise, Misc fee,<br>Early-bird|
|Collection › Bank|/FeeCollectionReports/|Br, Bank account,<br>Payment mode,DR,|Show; links to<br>Dishonoured,Cheque|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|submission form|BankSubmissionForm|Class, Cheque status|Statement|
|Collection › Online<br>Payments|/FeeCollectionReports/<br>RptOnlinePaymnetDetail<br>s|Br, FY, Account, Date<br>type, Gateway, Status<br>(Success / Failure / In<br>process / Refunds),<br>Consolidated / Detailed,<br>Device (Web / Mobile)|Show|
|Collection › Online<br>Payment Analysis|/FeeCollectionReports/<br>RptOnlinePaymnetDetail<br>s_NewFormat|Account, Location, Br,<br>Period|"Online Settlement<br>Desk"; export CSV,<br>XLSX, XLS, Print|
|Collection › Receipt<br>Book|/FeeCollectionReports/<br>FeeReceiptNoSearch|FY, Br, Fee category, Fee<br>type, Account, Mode,<br>Report type, Date,<br>Cancelled logic, AY,<br>Download type/range|CSV, Bulk download,<br>Print. Tabs: Receipt<br>book, Format 2, With<br>GST, Fee-type, Date-<br>wise, Account-wise,<br>Consolidated, Bulk, Fee<br>Abstract|
|Collection › Month<br>wise fee Collections|/FeeCollectionReports/<br>PopulateFinanceReports|AY, Br, Class type,<br>Classes,<br>Active/Inactive/All,<br>Transport<br>incl./excl./only|Tabs: Month-wise,<br>Payment-mode wise|
|Collection ›<br>Dishonoured<br>Cheques|/FeeCollectionReports/<br>DishonouredCheques|Br, Bank account, Date<br>basis, DR|Tabs: Bounced, Unpaid,<br>Repaid|
|Collection › Cheque<br>Statement|/FeeCollectionReports/<br>ChequeStatement|Br, Bank account, Date<br>basis, Cheque status|Show; DD statement|
|Collection › Fee<br>Transaction<br>Summary|/FeeCollectionReports/<br>RptFeeTransactionsSum<br>mary_Latest|—|Summary + details; old<br>report link|
|Collection › Fee<br>Balance Details|/FeeCollectionReports/<br>RptFeeBalanceReport|Br, Class type,<br>Installment, Fee type,<br>Late fee / LY due /<br>bounce charge, Account,<br>Status, Format<br>(consolidated /<br>individual),amount or %|Add/Remove columns.<br>Cols: Ref Code,<br>Student, Class/Sec,<br>Address, Mobile,<br>Father, Mother, Fee<br>type, Period, Balance,<br>Actual,Net,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||thresholds|Concession, Paid|
|Collection › Fee<br>Ledger Report|/FeeCollectionReports/<br>FeeLedger|Br, Class, AY, Mode, DR,<br>Status, Period / Receipt<br>wise|Show|
|Collection › Fee<br>Deposits Register|/FeeCollectionReports/<br>RptDepositesRegister|Br, Refundable / Non,<br>Deposit fee type,<br>Admission AY, Status|Get|
|Collection › Student<br>wise Fee payments<br>(AY)|/FeeCollectionReports/<br>RptStudentWiseFeePaym<br>entDetailsBetweenDates|Br, Classes, Mode, AY,<br>New/Existing, Account,<br>Fee category, Subtotals,<br>Fee type, Misc type, DR,<br>Advance adjustments|Show|
|Collection › Misc<br>Fee Collection<br>Details|/FeeCollectionReports/<br>MiscFeeCollection_Rpt|AY, Br, Class, Misc<br>group, Misc type, DR|Tabs: Transaction,<br>Group, Type, With tax|
|Collection ›<br>Download Bulk<br>Receipts|/FeeCollectionReports/<br>BulkTransactionsReports|AY, Br, Account, DR,<br>Mode, PDF / view|Bulk download, Print|
|Collection › Fee<br>head wise student<br>list|/FeeCollectionReports/<br>PopulateStudentFeeDeta<br>ils|—|Individual fee-head-<br>wise, Assigned fee-<br>head-wise|
|Collection › Other<br>Fee Collection<br>Details|/FeeCollectionReports/<br>ManageOtherFeeCollecti<br>onDetails|Location, Br, Paid by,<br>Period, Mode|Print, CSV, XLSX, XLS|
|Collection › Advance<br>Fee Paid Report|/FeeCollectionReports/<br>AdvanceFeePaidReport|AY, Br, Report type,<br>View (adjustments /<br>date / student /<br>detailed)|Show|
|Collection › FY-<br>Monthwise<br>Collection|/FeeCollectionReports/<br>FeePaymentReport|FY, Br, Class, Account|Get|
|Audit › Current<br>status of Previous<br>month OS|/FeeCollectionReports/<br>MonthWiseDueReport|Br, Class, Fee types,<br>Account, Month, Till /<br>On month, Status,<br>With/without late fee,<br>Consolidated/Summary,|Cols: Location, Branch,<br>Class, Sec, Enrollment,<br>Student, Father,<br>Mobile, Status, Total,<br>Concession,Net,Paid,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||carry-forward|Due|
|Audit › OS as at a<br>particular Month|/FeeCollectionReports/<br>PopulateClasswiseStuden<br>tFeeOutStanding|Br, Class, Fee types,<br>Month, Status, Format,<br>include Misc /<br>Application fee, carry-<br>forward|Get Report|
|Audit › Month wise<br>Concession|/FeeCollectionReports/<br>RptMonthWiseStudentC<br>oncession|Location, Br, Month, Cls,<br>Sec, Fee type, Status, Till<br>/ On month|Show|
|Audit › Cancelled<br>Fee Payments|/FeeCollectionReports/<br>CancelledFeePaymentDe<br>tails|FY, Br, Receipt /<br>Cancelled date, DR|Tabs: Detailed, Month-<br>wise, Reason-wise|
|Audit › Month wise<br>consolidate|/FeeCollectionReports/<br>PopulateMonthWiseStre<br>ngth_FeeType|Br, Service fee type,<br>Installment, Status|Tabs: Fee plan, Class|
|Audit › Fee Plan<br>details|/FeeDueReports/<br>FeePlanDetails|Br, AY, Segment, Normal<br>/ Transport, Fee-type /<br>Installment / Account<br>wise, Classes|Show|
|Audit › Fee<br>Transaction<br>Summary|(same as Collection)|—|—|
|Audit › Inactive<br>Students|/SISDasBoard/<br>InActiveStudentRollAudit|Br, Cls, Sec|Get|
|Audit › Consolidated<br>Misc Fee Details|/FeeCollectionReports/<br>ConsolidatedMiscfeeDet<br>ails|Location, Br, Misc<br>heads/types, Status|Show|
|Audit › Pre-<br>admission Details|/FeeCollectionReports/<br>StudentFrontOfficeDetail<br>s|AY, Br|Enquiries →<br>Registrations →<br>Admissions funnel|
|Audit/Due › Total<br>Paid and due (Dues<br>Eagle Eye)|/FeeDueReports/<br>RptTotalPaidDueReport_<br>DuePaidInstallmentDetail<br>s_Latest|Format, AY, Fee account,<br>Location, Br, more filters<br>(as on date, month,<br>custom range)|Columns & format<br>picker; export Excel,<br>CSV, Print/PDF; old 31-<br>column format|
|Audit › Admission<br>Details / Monthwise|(same as SIS reports)|—|—|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|strength||||
|Audit › Student Fee<br>Ledger|/FeeDueReports/<br>ManageMiscFeeLedgerR<br>eport|Location, Br, As on|Show|
|Audit › Consolidated<br>Monthwise OS|/FeeCollectionReports/<br>PopulateMonthWiseDue<br>Report_Consolidated|Apr–Mar / Jun–May,<br>Location, Br, Month, Fee<br>types, Status, carry-<br>forward|Show|
|Due › Class wise due<br>report|/FeeDueReports/<br>GetStudentDetails|AY, Br, Till installment,<br>Status, Paid on/before,<br>consider PDC /<br>scholarship, Admission<br>type, by installment no.<br>or due date|Show|
|Due › Branch wise<br>due report|/FeeDueReports/<br>FeeReport_New|AY, Location, Br, Fee<br>type, Misc type, Status,<br>Paid on/before, PDC, LY<br>dues, Fine, Day/Hostel,<br>Account|Show|
|Due › Fee Reminder<br>Slip|/FeeDueReports/<br>SendFeeReminderslips_C<br>ollectionFollowup_Main|—|Generate reminder<br>slips|
|Due › Batch and AY<br>wise Dues|/FeeDueReports/<br>RptBatchWiseYearlyDues<br>Report|Batch, AY, Br, Fee types,<br>scholarship (professional<br>colleges)|Get|
|Due › Fee<br>Outstanding|/FeeDueReports/<br>RptFeeOutstandingDues<br>Report|Br, Status|Show|
|Due › Due Fee<br>Details|/FeeDueReports/<br>RptDueReport|Location, Br, Classes, Fee<br>types, Occurrence (one-<br>time / installment /<br>monthly)|Show (100 rows) or<br>CSV|
|Due › Misc fee Due<br>Details|/FeeDueReports/<br>PopulateStudentMiscFee<br>Details|Br, Class, Misc group,<br>Misc type|Show|
|Due › Fee due|/FeeDueReports/|AY, Br, Installments, Fee<br>types,Consolidated/|Show|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|students count|FeeDueCount|Class wise||
|Due › Batch wise<br>Fee Due|/FeeDueReports/<br>RptBatchWiseDuesRepor<br>t|Br, Batch, Course, Fee<br>types, scholarship|Tabs: Detailed,<br>Semester-wise|
|Due › Branch Dues<br>and Concessions|/FeeDueReports/<br>RptAllBrancheDuesAndC<br>oncessions|AY, Location, Br, Class|Show, CSV|
|Due › Aging Due<br>Report|/FeeDueReports/<br>RptAgingDuesReport_Ma<br>in|Aging analysis format<br>1/2|Report|
|Due › Due with<br>scholarship|/FeeDueReports/<br>RptStudentscholarshipRe<br>port|Br, Class, Fee types,<br>Status, Segment|Get|
|Due › Month wise<br>Dues|/FeeDueReports/<br>RptMonthWiseDueRepor<br>t|AY, Br, Class, Status, Fee<br>type|Get|
|Due › Previous AY<br>Student Fee Dues|/FeeDueReports/<br>RtpAllPreviousAYStudent<br>FeeDues|Br|Refresh, Get|
|Due › All years Fee<br>due|/FeeDueReports/<br>RptClassWiseDuesReport|Br, Programme category,<br>Programme, Class, Fee<br>types, Caste, Segment,<br>Status, scholarship, fine,<br>AY|Get|
|Scholarship ›<br>Manage Types|/Finance/Scholarship|Br|Get|
|Scholarship › Assign<br>to Students|/StudentERP/<br>ScholarShipDetails|—|Tabs: Assigned, Not<br>assigned, Upload<br>disbursement|
|Scholarship › Details<br>Report|/Report/<br>RptSchloarshipFeeReceR<br>eport|AY, Br, Scholarship, Fee<br>types, Segment, Class|Tabs: Due, Detail|
|Log › Fee<br>Unassign/Change<br>Request|/Student/<br>FeeUnassignReport|AY, Br, Cls, Sec, Status,<br>Regular / Misc|Tabs: Unassign, Change<br>requests|
|Log› Fee Edit|/Finance/|AY,Br,Class,Fee type,|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Details|ChangeFeeInstallmentA<br>mount_Log|DR||
|Log › Change Fee<br>Plan Log|/Report/<br>RptChangeFeePlanLog|AY, Br, Cls, Sec|Show|
|Log › Update Fee<br>Payment Log|/Report/<br>RpStudentUpdateFeePay<br>mentLog|AY, Br, Cls, Sec|Show|
|Log › Fine<br>modification|/Report/<br>StudentDisableFineAmou<br>ntDetails_Get|Br, AY|Get|
|Log › Due Date<br>Change Log|/Report/<br>RptChangeStudentDueda<br>teLog|AY, Br, Cls, Sec|Show|
|Reports › AY<br>Collections|/FeeCollectionReports/<br>FinancialYearDashBoard|FY, Br|Show|
|Reports › Tally<br>Reports|/FeeCollectionReports/<br>TallyReportMainView|Tally format picker|Tally (Expenses),<br>Receivable|
|Reports › Cheque<br>Bounce|/FeeCollectionReports/<br>ChequeBounceDetailsRe<br>port_New|Br, Date basis, DR, Bank<br>account|Get|
|Reports › Child Care<br>Fee|/FeeCollectionReports/<br>MonthWiseCollectionFor<br>ChildCareFee|AY, Br|Tabs: Fee plan, Class,<br>Student consolidated,<br>Collection tracker,<br>Student detailed, On-<br>demand|
|Reports › Student<br>Projection|/FeeCollectionReports/<br>RptStudentProjectionRep<br>ort|AY, Br, Type, Cls, Sec,<br>Fee type, Status, As on,<br>LY due, Consolidated /<br>Detail|Show|
|Reports › Card<br>Swipe Charges|/FeeCollectionReports/<br>RptCardSwipeChargeDet<br>ails|Br, Bank, DR, Account,<br>Class, Credit / Debit|Show|
|Reports › Student<br>Excess Payments|/FeeCollectionReports/<br>ViewStudentExcessPaym<br>ents|Br, AY|Get|
|Reports › Staff|/FeeCollectionReports/|AY,Br,Staff|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Student Fee details|StaffKidsReport|||
|Reports › Last Year<br>Due (Promoted)|/FeeDueReports/<br>PromotedStudentsFeeBal<br>ance_LastYear|Location, Br, Status,<br>Regular / Misc|Search|
|Reports › Offline<br>Payments|/Finance/<br>RptRyanOnlinePaymentD<br>etails|Br, Class type, DR, Status|Get|
|Reports › Date wise<br>Monthly payments|/FeeCollectionReports/<br>Daywise_SummaryRepor<br>t|AY, Br, Dates|Get|
|Reports › Date wise<br>FY collections|/FeeCollectionReports/<br>RptGetFinancialYearColle<br>ctionByDate|Location, Br, FY, As on<br>date|Get|
|Reports › Quarter<br>and Month wise due|/FeeDueReports/<br>RptMonthWiseDueRepor<br>t_Format2|AY, Br, Class, Fee type|Get|
|Reports › ECS &<br>Parent Bank Details|/FeeCollectionReports/<br>ECSReport|AY, Br, Class, Date,<br>Installment, Account,<br>Father / Mother, PDC|Get|
|Reports › Accrual<br>Invoice Register|/Fee/<br>GetTaxInvoiceReports|FY, Br, DR|Get|
|Reports › Cheque<br>Statements|/FeeCollectionReports/<br>ChequeStatement_New|Br, Bank account, Date<br>type, DR|Show|
|Reports ›<br>Installment wise Fee<br>Invoice|/FeeCollectionReports/<br>RptMonthWiseReceivabl<br>eDueReport|AY, Br, Board, Classes,<br>Installments, DR|Show|
|Reports › Collection<br>Follow up|/FeeCollectionReports/<br>RptFeePaymentFollowUp<br>s|Br, Segment, User,<br>Follow-up date|Get|
|Reports › Ledger<br>Transaction|/FeeCollectionReports/<br>RptStudentFeeLedgerRep<br>orts|FY, Br, DR|Tab: Receipts Ledger|
|Reports › Lunch<br>Booking Details|/Library/LunchFeeDetails|Br, AY, Month, From–To<br>date, Student / Staff|Get|
|Reports ›|/FeeCollectionReports/|AY,Br,Exam fee type,|Tab: Transaction wise|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Examination Fees|ExaminationFeeCollectio<br>n_Rpt|DR||



### **School Store (uniforms, books, kits)** 

Catalogue hierarchy: Store Category (Regular Uniforms, Sports Uniforms, Text Books, Note Books…) › Item Category › Item (SKU, size). Kits bundle items per class or house group. Orders are paid online, cash-on-delivery or pay-at-school and delivered by MCB or the school. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Store › Organisation<br>Catalogue|/Inventory/<br>SchoolStoreCatalogue|Category (Shirts, T-Shirts,<br>Pants, Skirts…)|Add Item. Tabs:<br>Catalogue,<br>Items in<br>catalogue|
|Store › Manage<br>School Stores|/Inventory/SchoolStore|Store name, GSTIN, Delivery<br>by (MCB / School), Delivery<br>vendor, Address,<br>Country/State/City, Mobile,<br>Email, Receipt URL, Fee<br>account, Allow partial<br>payment, Allow individual<br>sale, Active|Add store,<br>Assign<br>branches, Kit<br>display settings,<br>Sale settings,<br>Payment<br>gateway,<br>Delivery<br>charges. Cols:<br>Store, Fee<br>account,<br>Receipt URL,<br>Branch,<br>Settings|
|Store › Store wise<br>Catalogue|/Inventory/<br>OrganisationStoreCatalogue|Organisation, Store|Get|
|Store › Uniform /<br>Other Kits|/Inventory/<br>PopulateClasswiseKitDetails|Class, AY, Store, Kit name,<br>Description, items sold<br>individually|Other kits|
|Store › House Group<br>Kit|/Inventory/<br>PopulateClassGroupwiseKit<br>Details|AY, House group, Store|Get|
|Store › Items to<br>Students|/Inventory/<br>PopulateStudentSearchforSt|Class, Sec, Status, Search by<br>(name / enrollment /|Assign items|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||oreItems|admission / father / roll)||
|Store › Item Sales<br>(POS)|/Inventory/<br>PopulateStudentSearchForC<br>artItems_Index|Br, Class, Sec, Status, Search<br>by, AY, Store category, Item<br>category, SKU code|Get items, Add,<br>Sale. Tabs:<br>Items Sale,<br>Address, View<br>Transactions|
|Store › Generate<br>Barcodes|/Inventory/<br>SchoolStoreItemBracodes|AY, Store, Category, Item<br>category, Item, Dimensions,<br>Copies|Generate|
|Store › Store Vendors|/Inventory/<br>InventoryVendorMaster|(same vendor master as<br>Inventory)|—|
|Store › Assign Items<br>to Vendor|/inventory/<br>PopulateSchoolStoreVendor<br>AssigningItems|Store, Category, Item<br>category|View assigned|
|Store › Books and<br>uniforms intimation<br>letter|/Inventory/<br>Rptstudentschoolstore|AY, Br, Class, Last date|Print letters|
|Orders › Date Wise<br>Orders|/Inventory/<br>SchoolCartItemsReport|Store, AY, DR|Get|
|Orders › Pending<br>Orders|/Inventory/<br>PopulateStudentSearchCash<br>OrderDetails|Class, Sec, Status, Search by|Search|
|Orders › Delivery<br>Details|/Report/<br>TextBookKitSaleDeliveryDet<br>ails|Br, Class, To be delivered /<br>Delivered|Bulk update<br>order status|
|Orders › Item Wise<br>Delivery Details|/Report/<br>ItemWiseSaleReportDelivery<br>Details|Br, Class, Delivery status, DR|Get|
|Orders › Packing Slip|/Inventory/<br>SchoolStorePackingSlip|Store, Branches, Order date|Get|
|Orders › PickUp<br>Request|/Inventory/<br>SchoolStorePickUpRequest|Store, Branches, Order date|Get|
|Base Line › Shoe<br>Measurement|/SchoolService/<br>SchoolStoreStudentShoeSize|AY, Br, Cls, Sec, Gender,<br>CMS / Inches|Get, Report|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Base Line › Uniform<br>Measurement|s<br>/SchoolService/<br>SchoolStoreStudentUniform<br>Sizes|Same|Measurement<br>report, Size<br>projection, Bulk<br>upload|
|Base Line › Assign<br>Language|/Student/<br>LanguageAssigningMaster|—|Second / third<br>language per<br>student (drives<br>book kits)|
|Base Line › Size Chart|/Inventory/<br>SchoolStoreSizeChart|Store, AY|Get|
|Offline › Offline<br>Deliveries|/Connect/<br>SchoolStoreOfflineDelivery|AY, Br, Search by (incl.<br>receipt no, transaction ID)|Search|
|Offline › Fee Paid<br>Students Offline<br>Delivery|/Connect/<br>SchoolStoreFeePaidStudents|AY, Br, Cls, Sec|Get|
|Reports › Student<br>Wise Projection|/Inventory/<br>PopulateStoreStudentsProje<br>ctionDetails|AY, Store|Get|
|Reports › Item Wise<br>Projection|/Inventory/<br>PopulateStoreItemsProjecti<br>onDetails|AY, Store|Get|
|Reports › Store Sale<br>Report|/Report/RptSchoolStoreSale|Store, Br, DR, Branch /<br>Vendor wise, Type<br>(datewise, consolidated,<br>detailed, item, gender…),<br>Gender, AY, categories,<br>Classes, Sections, Payment<br>mode|Show, CSV|
|Reports › Vendor<br>Wise Orders|/Inventory/<br>VendorWiseOrders_main|AY, Store, Br, Vendor, Order<br>status, Paid date|Show|
|Reports › Kit Wise<br>Sales|/Inventory/<br>RptUniformKitsSalesReport|AY, Br, Uniform / Other kit,<br>Kit|Get|
|Reports › Text Books<br>Issued|/Inventory/<br>KitSales_Rpt_Main|AY, Br, Kit, Class|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Reports › Order<br>Search|/Inventory/<br>Store_OrderSearch_Index|Store, AY, Enrollment code /<br>Transaction ID, dates|Get|
|Reports › Delivered<br>Report|/Report/<br>ItemDeliveryDetailsreport|Br, Class, Delivery source,<br>dates|Get|
|Reports › Assigned<br>Items Report|/Finance/<br>SchoolStoreItemToStudents<br>_ClassWise|AY, Br, Class|Get|
|Reports › Stock<br>Report|/Inventory/<br>SchoolStoreStockReport|Store, Category, Sub<br>category, Item category|Get; FY-wise<br>stock|
|Reports › Cash on<br>Delivery|/report/<br>RptSchoolStoreCODSales|Store, Br, DR, Branch /<br>Vendor, Gender, AY,<br>Category|Show, CSV|
|Reports › Pay at<br>School Sales|/report/<br>RptSchoolStoreSchoolAtDeli<br>verySales|Same + Already paid / Pay at<br>school|Show, CSV|
|Reports › School<br>Store Profit|/Inventory/<br>SchoolStoreProfitLoss|AY, Store, Br|Get|
|Reports › Text Books<br>Receivable|/Inventory/<br>RptPaidNotPaidStudentsRep<br>ort|AY, Br, Kit, Class, Paid / Not<br>paid|Get|
|Reports › Month wise<br>Store Sales|/FeeManagment/<br>SchoolStoreSaleGSTFileRepo<br>rt|FY, Store, Br|GST filing data|



### **Expenses Management (accounts / petty cash)** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Expense Mgmt › Chart of<br>Accounts|/PettyCash/<br>ChartofAccountsDetails|Br|Payment entry,<br>Receipt entry,<br>Vendor payments,<br>Voucher entry,<br>Bank accounts,<br>Manage parties,<br>Settings, Ledger<br>report. Tabs:<br>Other,Income,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||||Expense, Liability,<br>Asset|
|Expense Mgmt › Upload<br>Petty Cash Entries|/Finance/<br>UploadMoneySpent_New|Br, Petty cash<br>category, Ledger,<br>Mode (Cash /<br>Cheque), Bank, Bus<br>No, Excel file|Download format,<br>Validate, Upload|
|Expense Mgmt › Regular<br>Maintenance Bills|/StaffMenu/<br>BranchwiseperiodicBills|Br, FY|Tabs: Regular bills<br>setup, Bills,<br>Payments|
|Approvals › Approve<br>Expense Details|/Report/<br>PettyCashApprovals|Location, Br,<br>Assigned / All,<br>Remarks|Approve, Reject|
|Approvals › Approve Petty<br>cash Withdrawals|/Report/<br>PettyCashWithdrawApprov<br>als|Same|Approve, Reject|
|Approvals › Approve<br>Journal Vouchers|/Report/<br>PettyCashJournalApprovals|Same|Approve, Reject|
|Approvals › Approve Cash<br>Deposits|/PettyCash/<br>ApprovePettyCash|Location, Br, Type|Get|
|Reports › Balance Sheet|/Report/<br>RptBalanceSheetNew|Br, FY, Format 1–3,<br>Till date / DR|Income & Expense<br>account, Trial<br>Balance|
|Reports › Cash and Bank<br>Balances|/Report/<br>RptCashBankBalanceRepor<br>t|FY, Location, Br,<br>Cash / Bank, As on|Show|
|Reports › Branch Wise<br>Expenses|/Report/<br>RptBranchWiseLedgerRepo<br>rt|FY, Location, Br, DR|Show|
|Reports › Ledger Head<br>Expenses|/Report/<br>RptLedgerHeadExpensesRe<br>port|FY, Location, Br|Show|
|Reports › Consolidated<br>Cash Collections Balance|/Report/<br>RptConsolidateCashBalanc<br>eReport|FY, Location, Branch<br>status, Br, Collection<br>account, DR|Show|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Reports › Consolidated<br>Petty Cash Balance|/Report/<br>RptConsolidateBalanceRep<br>ort|FY, Location, Branch<br>status, Br, DR|Show|
|Reports › Day Sheet|/FeeCollectionReports/<br>RptIncomeExpenseDayShe<br>et|Br, DR, AY|Income + expense<br>day sheet|
|Reports › Journal Voucher<br>Report|/Report/<br>Expense_GeneralVoucherT<br>ally|Journal / Transfer<br>entry, Br, FY, DR|Show|
|Reports › FY Ledger Report|/Report/LedgerReport|Br, FY|Get|
|Reports › Final Account|/Report/<br>ExpenseManagementFinal<br>AccountReport|Br, FY, Based on<br>Receivables /<br>Receipts, DR|Get|



### **Finance Intelligence** 

|Group › Page|Endpoint|Filters /<br>inputs|Actions, tabs, columns|
|---|---|---|---|
|Intelligence ›<br>Advances and<br>Liabilities|/FeeDashBoard/<br>ManageFeeDuesIntellig<br>ence|Br|Cards: Current fee dues, Security deposits,<br>Unadjusted advances, Wallets|
|Intelligence ›<br>Student<br>Strength|/SISDasboard/<br>StudentStrength_Repor<br>ts_New|Br|Same 9 tabs as SIS strength report|
|Intelligence ›<br>Collection<br>Follow up|/Finance/<br>FeeCollectionFollowup<br>Tabs|—|Tabs: Collection follow-up, Send fee<br>reminders, Fee due Emails, SMS, WhatsApp,<br>Voice messages; Follow-up report, Fee<br>intimations|
|Revenue<br>Impact › Due<br>to Fee<br>unassign|/Finance/<br>ManageOverviewFeeU<br>nassignRequestDetails|—|Gross assigned → net receivable; by fee head;<br>fee head × installment; admission month ×<br>installment. Chart / Table. Cols: Request code,<br>Enrolment, Student, Class, Branch, Admitted<br>AY, Type, Date, Installment, ₹ unassigned,<br>Reason, Nature, Remarks, Attachment,<br>Requested, Ageing, State|
|Revenue<br>Impact › Due|/Student/<br>ManageOverviewActiv|—|Branch scorecard (strength, exits, attrition, net<br>loss,avg/exit), prorated revenue &projected|



|Group › Page|Endpoint|Filters /<br>inputs|Actions, tabs, columns|
|---|---|---|---|
|to Inactivation|eAndReactiveDetails||loss, month of exit → revenue forgone, by fee<br>component; Copy ledger as CSV|
|Revenue|/FeeDashBoard/|Regular|Concession dashboard|
|Impact › Due|ConcessionDashBoard_|/ Misc||
|to Concessions|Latest|fee, Br||



### **Admissions (CRM)** 

Pipeline: Lead → Enquiry (stages: Open, Close, Application Stage, Application Taken, Application Cancelled…) → Application / Registration (with fee) → Admission (Admission Form assigns class, section, admission type, fee) → Enrollment. Every record carries source (walk-in, website, digital campaign: Google/Meta/Twitter/LinkedIn, referral types), counsellor and follow-ups. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Enquiries › Upload<br>Enquiry|/Student/<br>UploadEnquiry|AY, Br, Admission type,<br>Class, Source ("How did<br>you know us"),<br>Counsellor, Stage,<br>Country, CSV file|Validate, Upload;<br>counts correct /<br>incorrect / duplicate /<br>existing|
|Enquiries › Upload<br>Application|/Connect/<br>UploadDirectAppliactio<br>ns|AY, Br, Admission type,<br>Class, Source, Country,<br>Payment mode,<br>Receiving account,<br>Online / Manual<br>receipt, file|Download format,<br>Validate, Error file,<br>Upload|
|Enquiries › Enquiries<br>Dashboard|/Student/<br>StudentFrontOfficeDB|AY, Location, Br, Team<br>staff, Month / Branch<br>wise|Funnel Enquiries →<br>Registrations →<br>Admissions|
|Enquiries › Daily MIS-<br>Admission Counsellors|/Report/<br>AdmissionCounsellorsD<br>ailyMis|Br, Month (last 12),<br>Counsellor|Get|
|Enquiries › Assign<br>Enquiries To<br>Counsellors|/Student/<br>AssignEnquiriesTocoun<br>sellor_Bulk|AY, Br, Counsellor,<br>Consolidated /<br>Detailed, Status, DR|Get → bulk assign|
|Enquiries › Admission<br>Form|/Student/<br>AdmissionForm_WebC<br>ustom_MDLevelFormat<br>2|AY, Br, From Enquiry /<br>Application / Direct,<br>Search by (enquiry<br>code, application no,|Search, Continue,<br>Submit, Print receipt.<br>Customised multi-step<br>admission form|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||name, mobile), Mobile,<br>Class, DOB, Ref code,<br>Application no/date,<br>Previous admission no,<br>Class, Section,<br>Admission type, Class<br>group, fee amounts,<br>Send SMS / Email||
|Enquiries › Send Online<br>Admission Link|/Student/<br>SendRegistrationPaym<br>entLink|AY, Admission / Paid<br>branch, Br, Class, Not<br>yet / Already sent|Get → send|
|Enquiries › Send Online<br>Registration Link|/Student/<br>SendRegistrationformli<br>nk|AY, Br, Class, Sent<br>status|Get → send|
|Enquiries ›<br>LeadSquared<br>Integration|/Organisation/<br>GetLeadSquaredIntegr<br>ationTabs|—|Integration settings<br>(not configured)|
|Enquiries › Merit<br>Students Enquiry<br>Upload|/Admission/<br>UploadEnquiry_Merit|Same as Upload<br>Enquiry|Tabs: Merit upload,<br>Landing Pages|
|Enquiries › New<br>Admissions Reporting<br>and Cancellations|/Admission/<br>ManageAdmissionRepo<br>rtingDateFeeRefunds|Admitted AY, Br|Reporting dates,<br>cancellations, refunds|
|Pre-adm › Followup<br>details|/FrontOffice/<br>FollowUpDetailsReport|AY, Br, Counsellor, Next<br>7 / 30 days / DR|Get|
|Pre-adm › Registration<br>Review|/Student/<br>PopulateRegistrationRe<br>views|AY, Br, With / without<br>cumulative, Date|Show;<br>Application/Registratio<br>n fee report|
|Pre-adm › Send SMS /<br>Email|/Admission/<br>AdmissionCampaigns|AY, Br, Grades,<br>Counsellor, Source,<br>Follow-up filter<br>(today / next 7 /<br>never / overdue),<br>Interaction date, DR|Get Data → Send<br>Email / SMS /<br>WhatsApp|
|Pre-adm › Pre-<br>Admission details|/<br>FeeCollectionReports/<br>StudentFrontOfficeDet|AY, Br|Funnel|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||ails|||
|Pre-adm › Cancelled<br>Enquiries|/Student/<br>CancelledEnquiry|AY, Br, Source, DR|Tabs: Enquiries,<br>Applications,<br>Admissions; cancel<br>reasons|
|Pre-adm › Registration<br>summary|/Report/<br>PopulateRegistrationsA<br>ndAdmissions|AY, Location, Br, Class<br>type|Tabs:<br>Application/Registratio<br>n, Admissions|
|Pre-adm › BDM Report|/Student/<br>EnquiryLeadsBDMRepo<br>rt|AY, BDM, Br|Get|
|Pre-adm › Enquiry<br>report|/Student/<br>EnquiryReport|Location, Br, Grade, AY,<br>Stage, Report type<br>(consolidated<br>branch/location,<br>detailed, format 2),<br>Entry type, Date|Get, Excel, Source-wise|
|Pre-adm › Front Office<br>DashBoard|/FrontOffice/<br>FrontOfficeDashBoard_<br>BDM|AY, Br, Counsellor, Date<br>type (entry / walk-in /<br>application), Status,<br>Source, DR|Get|
|Pre-adm › Duplicate<br>Entries|/Report/<br>DuplicateEntries_Repor<br>t|AY, Br, Source,<br>Enquiries / Leads, DR|Get|
|Pre-adm › Registrations<br>Report|/Finance/<br>MinimumCommittedA<br>mountReport|AY, Location, Br, Class,<br>DR|Get|
|Pre-adm › Digital<br>Source Campaign<br>Dashboard|/Report/<br>RptDigitalSourceWiseR<br>eport|Br, AY, Source (Google,<br>Meta, Twitter,<br>LinkedIn…), Campaign,<br>DR|Get|
|Pre-adm › Grade wise<br>Admission Analysis|/Report/<br>StudentGradeWiseAdm<br>issionAnalysis_Report|Location, Sub zone, Br,<br>AY|Get|
|Pre-adm › Front Office|/Report/|AY, Location, Br, DR,|Get|
|Summary|ApplicationDetails_Rep|Sort by date type||



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||ort|||
|Pre-adm › Enquiry<br>FollowUp Report|/Report/<br>EnquiryfollowupDetails|AY, Br, Source, Status,<br>Enquiry / follow-up<br>date, DR|Tabs: Consolidated<br>with final status,<br>Detailed follow-ups|
|Pre-adm › SourceWise<br>DashBoard|/Report/<br>SourcewiseLeadsandEn<br>quirysReport|Br, AY, Source type<br>(branch / online<br>forms / digital), Source,<br>DR|Tabs: Stage wise,<br>Parent visits|
|Pre-adm › Subjectwise<br>Online admission exam|/FrontOffice/<br>SubjectwiseOnlineadmi<br>ssionexamReport|AY, Br, Exam, DR|Get|
|Docs & Fields ›<br>Preadmission Student<br>Documents|/FrontOffice/<br>PreadmissionDocumen<br>tsandContractDetails|AY, Br|Tabs: Documents,<br>Completed application,<br>Concession pending|
|Docs & Fields › Class<br>wise Mandatory Fields|/Student/<br>AdmissionStudentMad<br>atoryFields|AY, Br|Mandatory admission<br>fields per class|
|MIS › Admissions<br>Master Dashboard|/Student/<br>RptMISDashboard|Location, Br, Pre-<br>admission AY,<br>Compared with AY, %<br>target increment|Tabs:<br>Enquiries/Applications/<br>Admissions<br>comparison, Master<br>dashboard, Finance<br>projections, School<br>vacancy|
|MIS › Monthly Deck|/Connect/<br>ViewBoardWiseEnquiry<br>Details_Main|Location, Br, AY|Board-wise monthly<br>deck|
|MIS › New Admissions|/<br>FeeCollectionReports/<br>RptAdmissiondts_Melu<br>ha|(same as SIS)|8 tabs|
|MIS ›<br>Application/Registratio<br>n Fee Details|/Report/<br>StudentAppandRegFor<br>msFeeDetails_Rpt|Location, Br, AY, Period|Tabs: Application,<br>Registration|
|MIS › Target Strength<br>Analysis|/Followup/<br>Preadmission_TargetSt|Location, Br, AY, DR,<br>Include cancelled|Target vs actual per<br>class|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||rengths|||
|MIS › Parent Walkin<br>Survey Response|/Followup/<br>ParentWalkinSurveyRe<br>port|AY, Br, Class, DR|Get|
|Approvals › Enquiry<br>Selection Approvals|/Followup/<br>ManageStudentObserv<br>ationFinalAssesments|AY, Br, Classes,<br>Remarks type (Final<br>assessment /<br>Discussion with<br>parent), Status|Approve / reject|
|Reports › Admission<br>Review|/Student/<br>PopulateAdmissionRevi<br>ews|AY, Br, DR|Get|
|Reports › Student<br>Dashboard|/SISDasboard/<br>StudentAnalysisReport|Br|Charts: gender, blood<br>group, transport…|
|Reports › Preadmitted<br>students list|/<br>FeeCollectionReports/<br>StudentEnrollmentRevi<br>ewsInfo|New / Re-admitted, AY,<br>Br, DR, Class, Month /<br>Grade wise|Tabs: Enquiries,<br>Applications,<br>Admissions, Cancelled<br>(new and re-admitted),<br>Consolidated, With fee<br>payments|
|Reports › Branchwise<br>School Leads|/Report/<br>SchoolLeadDetails|Location, Br, Type<br>(PRO), DR|Get|
|Reports › Sibling<br>Enquiry|/Student/<br>SiblingEnquiryReport|Br, Admission AY|Consolidated, Detailed|
|Reports › Admissions<br>Analysis|/Report/<br>PreAdmissionDashBoar<br>d|Location, Br, AY, DR|Get; Admissions<br>Performance|
|Reports › Hostel vs day<br>scholar|/Report/<br>hostelvsdayscholarsRe<br>port|AY, Br|Analysis|
|Reports › Admissions<br>Performance|/Student/<br>StatusWiseEnquiryRep<br>ort|AY, Br|Get|
|Reports › Counsellor<br>wise Followup|/Student/<br>CounsellorwiseFollowU<br>pReport|Location, Br, AY,<br>Enquiry / follow-up<br>date, Status, DR,|Tabs: by enquiry date<br>(2), follow-up date,<br>unique / cumulative|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||Consolidated / Detailed|counsellor activity|
|Reports › Agent wise<br>Followup|/Student/<br>TeleCallerorAgentwiseF<br>ollowUpReport|Location, Br, AY, Lead<br>status, DR, Type|Get|
|Reports › Registration<br>fee Adjustments|/Finance/<br>RptRegistrationFeeCon<br>vertToRegular|AY, Br, Classes|Show|
|Reports › Counsellor<br>wise Admission<br>Analysis|/Student/<br>CounsellorwiseAdmissi<br>onAnalysisReport|Location, Br, AY, DR|Get|
|Reports › Counsellor<br>wise Enquiry|/Student/<br>CounsellorAndSourceW<br>iseEnquiryReport|Br, AY, Stage,<br>Counsellor, Source, DR|Get|
|Reports › Referral<br>Report|/Admission/<br>RefferalSourceReport|AY, Br, DR|Tabs: Consolidated,<br>Outsiders,<br>Parent/Student,<br>Sibling, Staff, Outreach<br>partners, Friendship<br>schools, Brand tie-ups|
|Reports › Counsellor<br>Wise Admissions<br>Dashboard|/Admission/<br>CounsellorwiseAdmissi<br>onAnalysisDashboard|Br, Counsellor status,<br>Counsellors|Today / Week /<br>Month / Calendar year|
|Reports › Enquiries<br>Never followed up|/Admission/<br>NeverFollowupedRepor<br>t|AY, Br, Grades, DR|Get|
|Reports › Advaitel Call<br>log|/Admission/<br>AdvaitelLog_Main|Br, Call type (out / in /<br>missed), DR|Telephony log|



### **HR** 

Staff are split into Teaching, Non-teaching, Transport and Outsource departments, mapped to a Payroll Entity per school. Attendance comes from manual entry, biometric/RFID devices, face-recognition (FR) or GPS self check-in, with shifts (time-based or work-hours-based), sessions (morning / afternoon) and a 3-level reporting hierarchy for approvals. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Staff Details › Create|/HomeDasboard/|Br, Staff type, Location,|Add staff, inactivation|
|||Programme dept,Staff|request,activate. Tabs:|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Staff Details|StaffDisplay_Fast|dept, DR, Status,<br>inactive reason<br>(Retired,<br>Superannuation…);<br>column picker<br>(biometric code,<br>designation, gender,<br>DOB, mobile, email)|Active, Inactive,<br>Dashboard, Trained<br>staff, Work load,<br>Employment status,<br>Staff kids, Staff on<br>transport, Log,<br>Documents, Contract<br>staff, Superannuation.<br>Cols: Branch, Name,<br>Code, Unique ID,<br>Designation, Status,<br>Mobile, Email|
|Staff Details › Staff<br>Groups|/Staff/StaffGroupTypes|—|Tabs: Custom groups,<br>System groups,<br>Manage custom<br>groups, Staff roles|
|Staff Details › Inactive<br>Staff Approvals|/HomeDasboard/<br>GetInactiveStaffapprov<br>als|Br, Request DR|Get → approve|
|Staff Details › Update<br>Staff Details|/Staff/<br>UpdateStaffFullDetails|Br, Department, Status|Bulk edit grid|
|Staff Details › Staff<br>Trainings & PD|/Staff/<br>StaffProfdevelopement<br>Report|Br, dates|Trainings attended,<br>Professional<br>development,<br>Achievements &<br>milestones, Research<br>log, Add entry|
|Staff Details ›<br>Continuous<br>Feedback/Praises|/Staff/<br>StaffContinuousFeedba<br>ck|Br, Teaching / Non-<br>teaching, dates|Tabs: Activity, Give<br>feedback/praise|
|Staff Details › Manage<br>Outsource Staff|/Staff/<br>StaffTabwiseSalaryInfo<br>_OutSource|Br|Vendors, Contracts,<br>Map staff, Pay type|
|Staff Details › Staff<br>Handbook and Policies|/Student/<br>StaffOrgDocuments|—|Document list|
|Attendance › Give Daily<br>Attendance|/Staff/<br>CreateStaffAttendance|Br, Payroll entity,<br>Department, Date,|Get Staff, Morning /<br>Afternoon marking,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||Regular / Grid view|Update|
|Attendance › Shifts And<br>Sessions|/Staff/<br>ManageStaffShiftsSessi<br>onsAndAttendance|Br, Payroll month|Create shift. Tabs: Staff<br>with shifts, Time-based<br>in use / unused, Work-<br>hours-based in use /<br>unused, Weekly offs,<br>Dashboard, Branch<br>transfer staff|
|Attendance › Daily<br>Attendance Report|/Staff/<br>RptStaffAttendanceByT<br>ype|Br, Department, dates,<br>show in/out time|Tabs: Dashboard,<br>Present, Leave, Week<br>off, Absent, Timetable<br>substitution|
|Attendance › Monthly<br>Attendance Report|/Staff/<br>StaffAttendanceMonth<br>WiseReport|Br, Staff type,<br>Department, Payroll AY|Get|
|Attendance › Timing<br>Modification|/Staff/<br>StaffAttendanceTiming<br>Modifications|Br, Date, Department|Late/early adjustments<br>(biometric branches)|
|Attendance › Assign<br>Work From Home|/Staff/<br>StaffWorkFromHome|Br, Date type, From–<br>To, Department|Get → assign|
|Attendance › WFH<br>Attendance Marking|/Staff/<br>StaffWorkfromhomeAtt<br>endancemarking|Br, Date, Department,<br>remarks|Submit / Delete. Cols:<br>Shift, Session, Staff,<br>Code, Session time,<br>Punch time, Status,<br>Leave type, Remarks,<br>Biometric code,<br>Designation,<br>Department|
|Biometric › Staff<br>Biometric Codes|/Staff/<br>StaffBiometricCodeDat<br>a|Br, Department, Status|Map biometric/RFID<br>codes|
|Biometric › Late<br>Comers - Early Leaving|/staff/<br>populatestaffattendanc<br>ereports|Br, Department, DR,<br>Shift|Show|
|Biometric › Payroll<br>Biometric Attendance|/Staff/<br>RptBiometricAttendanc<br>eForAllStaffNew|Br, Payroll month, Staff<br>type, Department|Rules for lates / early<br>leaving, holiday +<br>weekoff|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Biometric › Daily<br>Biometric Attendance|/Report/<br>RptStaffBiometricAtten<br>dance|Br, Shift, Department,<br>Date, From–To|Staff shifts, Upload<br>biometric attendance,<br>Late comers|
|Biometric › Staff<br>Attendance<br>modification|/Staff/<br>StaffAttendanceModific<br>ations|Br, Department, Based<br>on timing / work hours,<br>Date, remarks, late flag|Tabs: Absent both<br>sessions, Half-day<br>absent, Present<br>late/early, Punches<br>beyond allowed, Half-<br>day present,<br>Leave/Holiday/WeekO<br>ff, Remarks, Less than<br>half day. Log report|
|Biometric › Modified<br>Attendance Report|/Report/<br>ModifiedBiometricAtte<br>ndence_New|Br, Department, Month|Tabs: Date wise, Staff<br>wise, Detailed|
|Biometric › Attendance<br>Between Dates|/Staff/<br>RptBiometricAttendanc<br>eForAllStaff_old|Br, Dates, Staff type,<br>Department|Get|
|Biometric › Approve<br>Regularizations|/Staff/<br>ManageStaffAttendanc<br>eRegularizations|Br, Payroll month,<br>Session (full / first /<br>second), Date|Approve|
|Biometric › Branch<br>Wise Daily Biometric|/Staff/<br>RptStaffBiometricAtten<br>dance_allBranches|Location, Br, Shift,<br>Department, Date|Show|
|Leaves › Create Staff<br>Leaves|/Staff/<br>CreateStaffLeaves_Mai<br>n|DR, Department, Br; HR<br>payroll months|Tabs: Leave types,<br>Leave category,<br>Category vs<br>Department,<br>Department vs<br>Category, Leave report,<br>Summary, Analytics|
|Leaves › Staff Holidays|/Staff/<br>CreateStaffHolidays_Ne<br>w|Year, All / Branch-wise,<br>Br, Leave category,<br>Department, From–To,<br>Description, Optional<br>holiday; payroll month<br>range|Add holiday|
|Leaves › Update Staff|/Staff/|Br,Category,|Tabs: Unassigned,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Monthly leaves|StaffMonthWiseLeaves<br>Update|Department, Paid leave<br>type, joining-date filter,<br>DR|Assigned (leave credit)|
|Leaves › Approve<br>Leaves|/Staff/ApproveLeaves|Level-3 / other level,<br>Br, Applied date,<br>Department|Show → approve|
|Leaves › Assign<br>Reporting Managers|/Staff/<br>AssignStaffReportingM<br>anagers|Br, Department type,<br>Department, Level|Get|
|Leaves › Approve<br>Comp-Off Credits|/Staff/<br>ApproveStaffSpecialLea<br>veApplications|Br|Add comp-off credit|
|Leaves › Staff Leave<br>Special Windows|/Staff/<br>CreateStaffHolidaysWin<br>dows_main|Payroll AY, Br|Add leave window|
|Leaves › Approve<br>Permission Requests|/FrontOffice/<br>ApproveStaffpermissio<br>ns|Br, Permission date,<br>Department|Tabs: Pending,<br>Approved / Rejected|
|Staff Tasks › Task<br>Manager|/Staff/StaffTaskData|—|Tabs: Teaching, Non-<br>teaching, Outsource<br>(designation-wise<br>recurring tasks)|
|Staff Tasks › My Team<br>Tasks|/Student/<br>ReportingManagerFeed<br>back|DR, Designation, Staff,<br>Frequency (daily /<br>weekly / monthly /<br>yearly), Task|Get|
|Staff Tasks › Task<br>Report|/Staff/<br>StaffDesignationTasksD<br>etailsReport|Br, Designation,<br>Frequency, Task,<br>Consolidated /<br>Detailed, Month, DR,<br>Include staff|Get|
|Staff Tasks › Task<br>Detailed Report|/Staff/<br>StaffDesignationTasksR<br>eport|Br, DR|Get|
|Staff Tasks › Task<br>Monitor|/Staff/<br>IndividualStaffwiseStaff|Br, Not done / Done,<br>DR|Tabs: Assigned by me,<br>Assigned to me|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
||Tasks_Main|||
|Reports › Staff Details<br>Report|/Staff/<br>RptStaffdetailsReportM<br>VC|Location, Br, Status,<br>Department type,<br>Department; column<br>groups Personal (DOB,<br>sex, marital,<br>anniversary), Contact<br>(emails, mobiles,<br>WhatsApp,<br>MS/Google), Family,<br>Address…|Add/Remove columns,<br>Show|
|Reports › MIS|/Staff/<br>StaffYearWiseActivean<br>dInactivecount|Br, Location, Year|Birthdays, Work<br>anniversaries, Inactive,<br>Joining, Print|
|Reports › Inactive Staff<br>Details|/Staff/<br>RptGetInActiveStaffList|Br, DR|Show|
|Reports › Staff<br>Inventory Issued Items|/Inventory/<br>GetStaffIssuedItems|(as Inventory)|—|
|Reports › Staff joining<br>details|/Staff/<br>RptStaffJoiningDetails|Br, Staff type,<br>Department, Status, DR|Show|
|Reports › Attendance<br>and Salary Log|/Report/<br>RptStaffLogReportDate<br>Wise|Br, Department, Dates<br>(max 180), Search by<br>(branch code / name /<br>biometric / ERP code),<br>Log type (timings /<br>salary)|Search|
|Reports › Sessions<br>Attended by Staff|/Staff/<br>ProfessionalStudentAtt<br>endanceByStaff|Br, Faculty, Month|Get|
|Reports › Staff Student<br>Fee details|/<br>FeeCollectionReports/<br>StaffKidsReport|AY, Br, Staff|Get|
|Reports › Staff Leaves<br>Report|/Staff/<br>RptStaffLeavesReportB<br>etweenDates|Location, Br,<br>Department, Status<br>(Approved/Rejected/Pe<br>nding/Cancelled/Delet<br>ed), HR AY|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Reports › Staff Leaves<br>Details|/Staff/<br>StaffLeavesReport|HR AY, Location, Br,<br>Department, Payroll<br>entity, Paid / Unpaid,<br>Status|Get|
|Reports › Reporting<br>Managers|/HomeDasboard/<br>staffhierarchyReporting<br>By|Br|Staff hierarchy Level 1<br>→ 2 → 3|
|Reports › Staff FR<br>Attendance|/Report/<br>RptStaffFRAttendance|Br, Shift, Department,<br>Date, From–To|Face-recognition<br>attendance|
|Reports › Staff<br>Attendance Report|/Staff/<br>RptStaffAttendanceByT<br>ype|(same as Daily<br>Attendance Report)|6 tabs|
|Reports › Staff Profile<br>Cards|/Staff/StaffProfileCards|Br, Department type,<br>Department, Profile<br>cards / Address labels|Print|
|Reports › Staff Kids<br>Report|/Staff/RptStaffKids|Working branch,<br>Student AY|Show|
|Reports › Roaming Staff<br>Details|/Staff/<br>GetRoamingStaffDetail<br>s|Date, Br, Department,<br>Staff|Get|
|Reports › Month Wise<br>Staff Leaves|/Staff/<br>StaffMonthonMonthLe<br>avesReport|Br, Category,<br>Department, Leave<br>type, Payroll month|Tabs: Selected month,<br>As on month|
|Reports › Staff<br>Replacement|/Staff/<br>StaffReplacements_Re<br>port|Br, DR|Get|
|Reports ›<br>Praise/Feedback/Comp<br>laints|/Staff/<br>StaffComplaintsandprai<br>seReport|Br, DR|Get|
|Reports › GPS Self<br>Check-in/out|/Report/<br>Onlinepunchoutpunchi<br>n|Br, Department type,<br>Department, Month|Show|



### **Staff Wall** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Staff Wall ›<br>Staff Wall|/Communication/<br>AdminStaffWallChat_M<br>ain|Message: Staff group, Topic<br>(Curriculum planning, PD, Event<br>prep…), Title, Branch, Description,<br>Attachment, Allow comments,<br>Emergency alert; Group: name,<br>department type, departments,<br>designations, access levels, all /<br>selected staff|Create message,<br>group, topic,<br>meeting; today's staff<br>birthdays|
|Staff Wall ›<br>Staff Groups|/Staff/<br>StaffCustomandSystem<br>Groups|—|Custom, System,<br>Manage, Roles|
|Meetings ›<br>Staff<br>Meetings|/Communication/<br>DaakiaOnlineMeetings|—|Scheduled,<br>Completed,<br>Cancelled, New<br>meeting (online via<br>Daakia)|
|Meetings ›<br>Staff<br>Meetings<br>Report|/Report/<br>RptStaffMeetingsandO<br>ppintments|Br, Meeting / Appointment, Online<br>/ Face-to-face|Show|



### **SMS** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|SMS › SMS<br>Templates|/Organisation/<br>ManageSMSTemplates<br>_New|DLT: Entity ID, Entity<br>name, Operator,<br>Sub-account, Header<br>ID, Header|Tabs: Default templates, DLT<br>approved templates, Short codes,<br>Custom templates|
|Send SMS ›<br>Send SMS|/SMS/SendSMS|Template list<br>(Admission, Alerts,<br>…)|Tabs: Class-wise, Section-wise, New<br>admissions, Class group, Transport,<br>Offline SMS, Customize, Login<br>details, Segment, Competitive<br>exam, Other exam marks,<br>Assignments, Parameterised<br>custom, Exam marks to all branches|
|Fee Due SMS<br>› Send Fee|/SMS/<br>FeeDueSMSInformatio|Rules: prefix "Dear<br>Parent",append|Tabs: Installment-wise, Fee due,<br>Customize,Zero-paid students,Due|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|due SMS|n|school name, length<br>limit|amount students|
|Fee Due SMS|/SMS/|Br|Send payment link|
|› Send Fee<br>Payment Link|SendFeeDueSMSPayme<br>ntLInk|||
|Reports ›|/Report/SmsLogReport|Branch / Class-|Failure reason codes|
|SMS Log||Section wise, Date,<br>Regular / Offline,<br>SMS type||
|Reports ›|/SMS/|Br, Location, Date,|Job-level delivery status|
|SMS Delivery|SMSDeliveryReport|SMS type, Class||



### **WhatsApp** 

WhatsApp sends use approved static templates (utility / transactional) via a BSP (AiSensy business projects; Haptik integration present but disabled). Most send pages share one pattern: Branch, Class, Section, recipients (Point of contact / Father / Mother / Student), template, message preview, then a student grid (Enrollment, Student, Father, Mother, each WhatsApp number, Message). Credits balance: 4,666. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Account › Balance<br>Recharge|/WhatsApp/<br>WhatsAppRecharge|Plan, Invoice account|Pay online.<br>Recharge history:<br>Amount, Txn ID,<br>Dates|
|Account › Templates|/Communication/<br>MCBWhatsAppTemplates_<br>DashBoard|Search|Templates<br>grouped by<br>module (SIS,<br>Finance, HR,<br>Transport, CBSE,<br>Admissions…)|
|Account › WhatsApp<br>Log|/Report/<br>WhatsAppLogReport|Br, dates|Get|
|Account › Create<br>Business Projects|/Connect/<br>GetAISensyBusinessList|Display name, Email,<br>Company, Contact,<br>Company size, Currency,<br>Timezone, Password,<br>Project name, Branch|Create project,<br>assign number to<br>branch|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Account › Manage<br>Parent WhatsApp<br>Numbers|/WhatsApp/<br>ManageWhatsNumberDeta<br>ils|Br, Class-section|Edit numbers|
|Haptik › Custom<br>Templates|/Communication/<br>Whatsapp_CustomTemplat<br>e|Name, Content, Type (Text<br>/ Image / Document /<br>Video), Active, For pre-<br>admission|Add / Update<br>(integration<br>disabled)|
|Haptik › Send<br>Message To Students<br>(+ with Files)|/Communication/<br>SendWhatsAppMessagefor<br>Students,<br>/SendhaptikWhatsAppNoti<br>fications|—|Disabled|
|Haptik › Send to<br>Preadmission<br>Students|/FrontOffice/<br>SendSMStoWhatAppoptinS<br>tudents|Open enquiries /<br>Applications taken|Disabled|
|Haptik › Preadmission<br>Opt-in Report|/Report/<br>Whatappoptinstudentsrep<br>ortforEnquiry|Location, Br, AY, Enquiry /<br>Application, Stage|Get|
|Custom › Send Special<br>Message|/Communication/<br>SendWhatsAppSpecialMess<br>agetoStudents|Common pattern + file<br>attachment|Get Students,<br>Preview & Send|
|Attendance › Period<br>wise Absent Message|/Communication/<br>SendWhatsAppMessagetoA<br>bsentStudents_Periodwise|Common pattern + Date|Preview & Send|
|Attendance › Student<br>Absent Message|/Communication/<br>SendWhatsAppMessagetoA<br>bsentStudents|Common pattern +<br>Timings, Date|Preview & Send|
|Attendance › Student<br>Biometric/RFID<br>Attendance|/Communication/<br>SendWhatsAppMessagetoB<br>ioMetricandRFIDAttendanc<br>e|Common pattern +<br>Timings, Date|Extra col: Punch<br>date-time|
|Attendance › Staff<br>Biometric Attendance|/Sms/<br>SendStaffWhatsAppMessag<br>etoBioMetricandRFIDAtten<br>dance|Br, Department, Date,<br>Template|Cols: Branch<br>code, Biometric<br>code, Name,<br>Department,<br>Designation,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||||WhatsApp, Punch<br>time|
|Login Details › Send<br>Login details|/Communication/<br>SendLoginDetailstoWhatsA<br>pp|Br, User type,<br>Department, Classes,<br>Sections, Student type<br>(incl. never logged in),<br>Template, Mother/Father,<br>All / never-logged users,<br>Prefix message|Cols: Student,<br>Enrollment,<br>Username,<br>Password,<br>WhatsApp<br>numbers, Alias,<br>Class, Sec|
|Fee Due › Fee Due<br>WhatsApp Message|/WhatsApp/<br>FeeDue_WhatsAppTemplat<br>eMessage|Br, Static template / Reply<br>to parent (24-hour<br>window), User type,<br>Template, Date, Cls, Sec,<br>Term, Fee types, Fine<br>amount|Continue →<br>preview|
|Others › Transport /<br>Online Classes /<br>Examination / PTM /<br>Events / Grade Book<br>messages|/WhatsApp/Transport_…,<br>Online_…, Examination_…,<br>PTM_…, Events_…,<br>WhatsappGradeBook|Same template form +<br>module-specific filters<br>(route, class group,<br>attendance type, event<br>type, evaluation, exam,<br>month)|Continue →<br>preview|
|Communication ›<br>WhatsApp<br>Announcement|/WhatsApp/<br>WhatsappAnnouncement|Date range,<br>Announcement type|Push<br>announcements<br>(approval by<br>coordinator /<br>principal)|
|Communication ›<br>WhatsApp Diary|/WhatsApp/WhatsappDiary|Br, Class-Section,<br>Template|Continue|
|Communication ›<br>WhatsApp<br>Assignments|/WhatsApp/<br>WhatsappAssignments|Br, User type, Template,<br>Date, Cls, Sec, Subject|Continue|
|Communication ›<br>Student Birthday<br>Wishes|/WhatsApp/<br>WhatsappBirthDay|Br, User type, Template,<br>Class-Section, Date|Continue|
|Two-Way › Reply<br>Parent Messages|/Communication/<br>WhatsAppIncomingMessag|Location, Br, Last 24h /<br>Today / 7 / 30 days / DR,|Get → reply|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||esReport|Replied / Not||
|Two-Way › Reply in|/Communication/|Br, Cls, Sec, Subject, Last|Get|
|Bulk|SendWhatsAppReplyBulkM<br>essagestoParents|24 hours||
|Two-Way › WhatsApp|/Report/|AY, Br, Status|Get|
|alerts opt-in|Whatappalertsoptinreport|||



### **Email** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Templates ›<br>Admission Email<br>Templates|/Organisation/<br>EmailTemplates|Br|Template types: Enquiry,<br>Application, Registration,<br>Admission, Pre-admission<br>exam, Re-admission,<br>Admission link, Login<br>credentials, Registration link,<br>Leads, Walk-in survey,<br>Scheduled visits, Walk-in<br>completed, General. Create /<br>Default template|
|Templates ›<br>Student Contract<br>and Other|/Organisation/<br>EmailTemplates|Br|Absent, Late, New / Existing<br>student contract form,<br>General|
|Templates › Fee<br>Reminder Email<br>Templates|/Communication/<br>EmailDefaultTemplates|—|Tabs: Default, Customised|
|Templates ›<br>Enquiry<br>Campaign<br>Templates|/FrontOffice/<br>CampaignEnquiryesTe<br>mplate|AY, Active / Inactive|Add campaign (drip), view<br>template|
|Templates ›<br>Enquiry Followup<br>Campaigns|/FrontOffice/<br>FollowUPCampaignTe<br>mplates|AY, Status|Add follow-up campaign|
|Templates › Staff<br>General Email<br>Templates|/Communication/<br>StaffEmailTemplates|Br|Create / Default|
|Templates ›|/HomeDasboard/|Organisation/Branch|Update signature,Test email.|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Email settings|EmailSettings|level; from email per<br>department<br>(@myclassboard.in),<br>signature|Cols: Type, Status, From,<br>Signature|
|Templates ›<br>Greetings Gallery|/Communication/<br>AutomatedEmailGreeti<br>ngTemplates|—|Tabs: Student / Staff / Parent<br>birthday, Staff work<br>anniversary, Staff / Parent<br>marriage anniversary|
|Send › Send<br>Email|/Communication/<br>SendEmailTabs|Br|Tabs: General, Individual<br>student, Login details,<br>Segment/Class group,<br>Transport students, New<br>admissions, Hostel,<br>Competitive exams, General<br>template, Transport info,<br>Login details custom|
|Send › Send<br>Email To Staff|/Communication/<br>SendEmailToStaffTabs|Br|Tabs: General, Login details,<br>Staff groups, Staff templates|
|Send › Send<br>Custom Email|/Communication/<br>SendCustomEmail|Br, Type, From, To, Cc,<br>Bcc, Subject,<br>Description (AI assist),<br>Attachments (3MB)|Send|
|Send › Email to<br>Group Students|/Student/<br>SendEmailToStudentGr<br>oups|AY, Br, Group status|Tabs: Academic, House,<br>Practical, Finance, Store,<br>Custom, Clubs, ECA, Project,<br>System tags|
|Fee Due › Fee<br>due Email with<br>Payment Link|/Communication/<br>SendEmailtoFeeDueStu<br>dents_CollectionFollow<br>up|Br, From, Programme,<br>Classes, Sec, Status,<br>Installment / Fee-type<br>wise, include ECS,<br>Regular / Misc /<br>Bounce charges,<br>Category, show fine /<br>delay days / due date /<br>online link, recipients|Next → message → Send|
|Fee Due › Send<br>Fee Reminder<br>slips|/FeeDueReports/<br>SendFeeReminderslips<br>_CollectionFollowup|Br, Programme,<br>Classes, Sec, Reminder<br>template, Installment /<br>Month / Due-date|Custom reminder format|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||wise, Regular / Misc, LY<br>due, Due amount ≥ /<br>> / zero paid, Reminder<br>date, Due date, copies<br>per row, rows per page||
|Reports › Email<br>Log|/Report/<br>EmailLogReport_New|Dates, Email type|Usage, Campaigns log,<br>Delivery status checker|
|Reports › Email|/Communication/|Branch / Type wise|Get|
|Usage|EmailUsageReport|||
|Reports ›<br>Preadmission|/Report/<br>GetPreadmissionCamp|Br, Enquiry / Follow-up<br>campaign, DR|Get|
|Campaigns log|aignsEmailLog|||



### **Voice Calls** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Click to Call › Click to<br>Call|/SMS/<br>ClickToCall_Kaleyra|Br, DR|Call log (Kaleyra)|
|Click to Call › Agents|/Report/<br>RptDirectCallAgents|—|Cols: Branch, Click-to-<br>call number, Agent<br>name/email/mobile,<br>Dialer<br>username/password|
|Voice Message ›<br>Subscribe/Recharge|/SMS/SubscribeAPIkey|Plan, Invoice account|Tabs: Pay online,<br>Recharge history,<br>Delivery log|
|Voice Message › Text<br>To Speech|/SMS/<br>SendVoiceSMS_Tabs|—|Tabs: Existing students,<br>Absent students, New<br>admissions, Open<br>enquiries|
|Voice Message › Fee<br>Due Voice Message|/SMS/<br>FeeDueVoiceSMSInfor<br>mation|—|Tabs: Installment-wise,<br>Fee due, Customize,<br>Zero paid, Due amount<br>(not subscribed)|
|Voice Message ›<br>Schedule Voice<br>Message|/SMS/<br>SendScheduledVoiceS<br>MS|Br|Schedule new|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Voice Message › Voice<br>Clip|/SMS/<br>Send_Clip_VoiceSMS|Br, User type, Class-<br>Section, Department,<br>Father/Mother/Guardi<br>an, Gender, Transport,<br>Category|Manage clips, Continue|
|Reports › Voice API|/Report/|Br, Date|Show|
|(bridge calls) Log|RptClickTocallAPILog|||
|Reports › Call log|/Report/|All / Answered /|Show|
|Report|RptDirectCallReports|Missed, Br, Date||



**Diary, Announcements, Calendar, Gallery, Notifications, Student Wall** 

|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Diary › Student Diary<br>(Class Room)|/Connect/<br>ClassRoomActivityDetails_Lat<br>est|Br, Month, Cls,<br>Sec|Class diary, activities,<br>events & competitions|
|Diary › Approve Diary|/Communication/<br>ApproveStaffDairy|—|Tabs: Pending,<br>Approved, Auto-<br>approved (only if<br>approval setting on)|
|Diary › Students Diary<br>Report|/Report/<br>RptGetOverallDiaryReport|Location, Br, This<br>month /<br>Between dates,<br>Table / Grid /<br>Grid<br>consolidated|Green = approved, red<br>= pending; date-wise|
|Diary › Student Diary<br>Submissions|/Communication/<br>StudentDiarySubmission|Br, Diary date|Get|
|Announcements ›<br>Announcement Types|/Organisation/<br>GetAnnouncementTypes|Name, Icon<br>colour, Branch-<br>level users,<br>Subject related,<br>Circular, Staff<br>related,<br>Approval needed<br>/ Direct|Add. Cols: Type,<br>Colour, flags, Actions|
|Announcements ›<br>Announcements|/Communication/<br>CreateAnnouncement_New|Date range,<br>Type, Applicable|New announcement;<br>send via Email /|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||to|WhatsApp|
|Announcements ›<br>Approve<br>Announcements|/Communication/<br>ApproveStaffAnnouncements|—|Pending, Approved,<br>Auto-approved|
|Announcements › Staff<br>Announcements|/Communication/<br>CreateAnnouncement_Staff_<br>New|Date range, Type|New staff<br>announcement, via<br>Email|
|Announcements ›<br>Policies and Handbooks|/Student/<br>StudentHandBookdetails|AY|Documents|
|Announcements ›<br>Announcement Report|/Report/<br>AnnouncementDetailsReport<br>_new|AY, Br|Search|
|Calendar › Calendar|/Communication/<br>EventCalenderAcademicYear<br>Wise_Rpt|AY, Br, Class|School calendar;<br>Manage event types,<br>Vacations, Holiday list|
|Calendar › Exam<br>Calendar|/Communication/<br>ViewExamCalenderAcademic<br>YearWise|AY, Br, Class|Calendar view|
|Calendar › Class<br>Calendar|/Communication/<br>EventCalenderAcademicYear<br>Wise_Class_Rpt|AY, Br, Cls, Sec,<br>Type|Get|
|Calendar › Student<br>Birthday Calendar|/Communication/<br>EventCalenderBirthdays|Br, Cls, Sec,<br>Month; email<br>form (template,<br>from, to, cc,<br>subject, greeting<br>image,<br>attachments)|Send bulk SMS /<br>Email / WhatsApp.<br>Cols: Photo, Student,<br>Branch, Class, Section,<br>Mobile|
|Calendar › Staff Birthday<br>Calendar|/Communication/<br>BirthdayCalenderForStaff|Br, Staff type,<br>Month; same<br>email form|Send SMS / Email /<br>WhatsApp. Cols:<br>Photo, Staff, Branch,<br>Designation, Mobile|
|Gallery ›<br>Activities/Photo Gallery|/Communication/<br>ManageCreateActivityDetails|AY, Br, Activity<br>type (General,<br>Subject-wise,<br>House,Club,|Create activity album|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|||ECA, Events)||
|Gallery › Approve Photo<br>Gallery|/Communication/<br>ApproveStaffPhotoGallery|—|Pending, Approved|
|Gallery › Group Photos|/Report/<br>StudentClassGroup_NewPhot<br>os|Br|Get|
|Gallery › Students<br>Profile Album|/Student/<br>RptStudentProfileAlbum|Br, Class|Get|
|Gallery › Staff Wise<br>Classroom Activity|/Staff/<br>StaffwiseActivityCountDashB<br>oard|AY, Br|Get|
|Gallery › Activity Album|/Communication/<br>GetAcivityAlbumImages|AY, Br, Cls, Sec|Get|
|Notifications › Fee<br>Notifications|/SMS/<br>SendAblyFeeDueNotifications|—|Installment-wise, Fee<br>due, Customize, Zero<br>paid, Due amount,<br>Manage (app push via<br>Ably)|
|Notifications ›<br>Gradebook Notifications|/SMS/<br>SendAblyGradeBookNotificati<br>ons|—|Other exam marks,<br>Objective exam marks|
|Notifications › Push<br>Transport Notifications|/Report/<br>SendTransportNotificationBy<br>Route|Br, Single /<br>multiple routes,<br>Route, Stop,<br>Pickup / Drop,<br>User type,<br>Department,<br>Classes,<br>Sections,<br>Message, Link|Get count, Preview &<br>Send. Cols: Name,<br>Devices count, Mobile,<br>Class, Section|
|Notifications › Absent<br>Students|/Communication/<br>SendNotificationtoAbsentStu<br>dents|Br, Timings, Cls,<br>Sec, Absent<br>reason, Date|Get, Send|
|Notifications › Push<br>Customized|/Communication/<br>SendSpecialInformation_Noti<br>fy|—|General, Transport,<br>Competitive exam,<br>Birthday|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs, columns|
|---|---|---|---|
|Notifications › Channels<br>List|/Communication/<br>RptGetAblyChannelSubscribe<br>dList|Br|Subscribed devices|
|Notifications ›<br>Notifications Report|/Report/RptJobNotifications|Br|Automated, Manual<br>push|
|Student Wall › Student<br>Wall Report|/Communication/<br>MessageReport|Location, Br, Cls,<br>Sec, DR|Tabs: Not replied,<br>Tagged, All messages|
|Student Wall › Class<br>Wall Report|/Communication/<br>ClassWallAcademicYearWise<br>_Rpt|AY, Br, Class|Group messages|
|Student Wall › Manage<br>Class / Student wall|/Organisation/<br>SchoolChatGroupIntegration<br>Settings|—|Toggle auto-posting<br>into walls|
|Student Wall › Manage<br>Subject Groups|/Organisation/<br>ManageGroups|Br|Get|
|Student Wall › Chat<br>Settings|/Organisation/ChatSettings|Access level|Which staff users<br>parents/students can<br>chat with|



### **CBSE and State (Gradebook)** 

Gradebook model: Structure (per AY + branch) › Parts (Scholastic / Co-scholastic) › Terms › Evaluations › Exam Types › Tests per subject, with grading scales, skills, remarks indicators and a Master Examination Scheme (report-card logic). Report cards come from templates with term or evaluation publish settings. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Grade Book › Structure<br>Creation|/GradeBook/CCEStructure|AY, Br|Get → terms /<br>evaluations /<br>parts|
|Grade Book › Master<br>Examination Scheme|/GradeBook/<br>ManageExaminationSchem<br>e_Master|Board, AY, Structure|Weightage /<br>calculation logic|
|Grade Book › Grade|/GradeBook/|Structure, Part|Skills per subject|
|Book Skills|CreateSubjectSkills_New|||
|Grade Book › Create|/GradeBook/|—|Cols: Exam type,|
|Exam Types|CreateCCEExamTypes||Sequence|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Grade Book › Student<br>Remarks Indicators|/GradeBook/<br>StudentRemarksTypes|Category, Grade<br>(applicable / not),<br>Description, Indicator<br>statements|Add category /<br>grade /<br>statement,<br>assign defaults|
|Grade Book › Scholastic<br>Test Marks Entry|/GradeBook/<br>TestMarksEntryCreation_M<br>DLevel|Scholastic / Co-scholastic,<br>Br, Cls, Sec, Term,<br>Subject, Evaluation,<br>accept grades, Enter /<br>Upload|Get → marks<br>grid; upload<br>format|
|Grade Book › KYA<br>(Aptitude Tests)|/Student/KYATestResults|AY, Br, Board, Class-Sec|Get|
|Settings › Update<br>Results for Term<br>Report Card|/GradeBook/<br>UpdateMarkforReportCard|AY, Br, Class, Term, Type<br>(parent subjects, class<br>highest, rank…)|Post computed<br>results|
|Settings › Update<br>Results for Evaluation<br>Report Card|/GradeBook/<br>UpdateMarkforReportCard_<br>Evaluation|Same|Post results|
|Settings › Evaluation<br>Report Card Publish|/GradeBook/<br>ParentReportCardEvaluatio<br>nSettings|Br, Class, Term,<br>Evaluation; publish date,<br>enable for parents|Get|
|Settings › Term Report<br>Card Publish|/GradeBook/<br>ParentReportCardSettings|Br, Term; publish date,<br>reopen date, enable|Get|
|Settings › ReportCard<br>Templates|/GradeBook/<br>AvaliableReportCardFormat<br>s|—|Tabs: School<br>template, URL<br>setting, MCB<br>term template<br>gallery, MCB<br>evaluation<br>template gallery|
|Subject Outcomes ›<br>Subject Outcomes|/GradeBook/<br>CoCurricularSubjectStrands|Board, Programme,<br>Classes|Strands /<br>outcomes|
|Subject Outcomes ›<br>Branch Specific|/GradeBook/<br>BranchSpecificSubjectOutco<br>mes_CBSE|Br, Board, Programme,<br>Classes, All / Academic /<br>Co-curricular|Get|
|Subject Outcomes ›|/GradeBook/|Br, Class, Board,|Add grade|
|Statements & Grading|AssignSubjectOutComeGrad|Programme,Scale name,|boundaries,|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Scale|ingScaletoClass|grades (grade, point,<br>ranges, remarks)|new scale|
|Subject Outcomes ›<br>Grade Entry Status|/ReportAnalysis/<br>SubjectOutcomeGradeEntry<br>Status|Br, Class, Term, Subject|Get|
|Other Exams › Create<br>Examinations|/Examination/<br>CreateOtherExaminations|AY, Class category,<br>Classes, Month|Tabs: Manage<br>exams, Grading<br>scale, Academic<br>class groups;<br>Create exam|
|Other Exams › Marks<br>Entry Dashboard|/Examination/<br>OtherExaminationsDashboa<br>rd|Br, AY, Month, Class /<br>Group wise, Group, Class|Get|
|Other Exams › Analysis<br>Reports|/Examination/<br>RptotherExamReports_Mai<br>n|Exam report / % breakup|View grading<br>scale|
|Other Exams ›<br>Comprehensive<br>Reports|/Examination/<br>OtherExamsAnalysisReport|Br, AY, Type, Group, Cls,<br>Sec, Exam|Show|
|Competitive ›<br>Competitive Exams|/Examination/<br>CreateCompetitiveExamTyp<br>es_New|AY|Add exam<br>(Olympiads etc.)|
|Competitive › Student<br>Result|/Examination/<br>StudentAcademicIPEExamD<br>etails|Br, AY, Exam|Get; exam-fee<br>report|
|Competitive › Hall<br>tickets Report|/Examination/<br>RptStudentsHallTickets_org|AY, Location, Br, Class<br>type, Class, Exam|Show, CSV|
|Reports › Test Wise<br>Analysis|/CCEReportCard/<br>RptCCETestWiseAnalysisRep<br>ortCharts|Br, Cls, Sec, Term,<br>Evaluation, Subject type,<br>Subject, Test type, Test,<br>Students, Status,<br>Category, Format; column<br>toggles (%, grade, totals)|Get (charts)|
|Reports › Report Card<br>Viewers|/CCEReportCard/<br>RptReportCardViewers|Br, AY, Class-Sec, Format|Which parents<br>viewed|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Reports › Evaluation<br>Report|/Report/<br>RptCCEEvaluationReport|Br, Class-Sec, Term,<br>Evaluation, Subject type,<br>Subject, Analysis, include<br>father/mother/IDs|Show, Columns|
|Reports › Term Wise<br>Analysis|/ReportAnalysis/<br>RptTermWiseAnalysisRepor<br>t|Br, Class-Sec, Term,<br>Subject type, Subject,<br>Evaluation, Exam type|Tabs: Report-<br>card logic,<br>Analysis|
|Reports › Teacher Wise<br>Analysis|/CCEReportCard/<br>TEACHERWISESTUDENTANA<br>LYSIS|Br, Class-Sec, Term,<br>Evaluation, Subject, Staff|Grade-wise<br>counts, top<br>students|
|Reports › Subject and<br>Class Wise|/CCEReportCard/<br>RptDeptandsubjectwiseAnal<br>ysis|Br, Cls, Sec, Term,<br>Evaluation, Subject,<br>Format, Status|Show|
|Reports › Class Exam<br>Topper|/AcademicPlanning/<br>ClassTotalResultTopper|Br, Cls, Sec, Term,<br>Evaluation, Subject type,<br>Subject, Show in report<br>card|Tabs: Logic,<br>Subject toppers|
|Reports › Report Card<br>Analysis|/GradeBook/<br>ReportcardAnalysis|Location, Br, Cls, Sec,<br>Group, Term, Subject,<br>Format 1–4, column<br>toggles|Show|
|Reports › Overall Result<br>Analysis|/CCEReportCard/<br>RptOverallResultAnalysisRe<br>port|Location, Board, Br, Class|Get|
|Reports › GPA Wise<br>Exam Analysis|/CCEReportCard/<br>GPAWiseExamResultAnalysi<br>s|Br, Marks / Graph /<br>Percentages|Show|
|Reports › Subject Wise<br>Analysis|/CCEReportCard/<br>RptSubjectWiseAllBranches<br>Analysis|Br, Class, Term,<br>Evaluation, Subject type,<br>Subject|Max, count,<br>grade<br>distribution,<br>average|
|Reports › Competitive<br>Exam Hall tickets|/Examination/<br>RptStudentsHallTicketsStatu<br>s|AY, Location, Class type,<br>Class, Exam|Get|
|Reports › Language and|/Report/<br>StudentLanguageAndOption|Br|Show|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Optional Subjects|alSubjectCounts|||
|Reports › Branch<br>Shuffled Report card|/Student/<br>BranchShufflingStudentRep<br>ortCard|Br, AY, Period|Show|
|Reports › Other<br>Examinations<br>Attendance|/Examination/<br>OtherExamAttendateReport<br>ByExamination|Group, Class, Exam|Get|
|Reports › Evaluation<br>Marks Analysis|/ReportAnalysis/<br>RptCCEExaminationsMarksA<br>nalysis|Br, Class-Sec, Term,<br>Evaluation, Exam type|Tabs: Logic,<br>Report, Marks<br>register, Class<br>teacher<br>remarks,<br>Subject remarks|
|Reports › Marks Entry<br>Status|/CCEReportCard/<br>StudentMarksEntryStatus|Br, Class, Term,<br>Evaluation, Format|Green / red tick<br>per test|
|Reports › Result<br>Analysis Report New|/ReportAnalysis/<br>RptEvaluationWiseAnalysisR<br>eport|Br, Cls, Sec, Term,<br>Evaluation, Subject type,<br>Subject|Tabs: Logic,<br>Grade files,<br>Consolidated<br>marks sheet,<br>Grade-wise,<br>Subject-wise,<br>Section-wise,<br>Class<br>performance,<br>Toppers, Marks<br>register,<br>Formula view,<br>Outcomes, Class<br>teacher<br>remarks,<br>Subject remarks|
|Reports › Master<br>Examination Scheme<br>Reports|/ReportAnalysis/<br>BranchAnalysisReportsBase<br>dOnReportCardLogic|Board, AY, Class|Get|



### **ECA and PET** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|ECA › Manage ECA<br>and PET Schedules|/GradeBook/SkillActivity|ECA / PET, Type<br>(Indoor / Outdoor /<br>Activity), Name,<br>Sequence|Tabs: ECA/PET,<br>Learning stages|
|ECA › ECA Grading<br>Scale|/GradeBook/<br>StageActivityGrades|ECA / PET scale,<br>Activity, Grade, Point,<br>Remarks|Add, grade<br>statements|
|ECA › Assign ECA /<br>PET To Branches|/GradeBook/<br>AssignSkillActivityToBranch<br>es|Location, AY, ECA / PET,<br>Type, Skill name,<br>Sequence|Add skill & skill set|
|ECA › Assign ECA /<br>PET To Classes|/GradeBook/<br>AssignSkillActivityToClasses|Br, AY|Mapping grid|
|Health › Student<br>Health Details|/GradeBook/<br>CreateStudentHeightandW<br>eight|Br, Class-Sec|Tabs: Term-wise<br>report & entry,<br>Month-wise report<br>& entry, Blood<br>groups,<br>CWSN/PH/Gifted<br>(height, weight,<br>BMI)|
|PET › Physical<br>Education Structures|/GradeBook/<br>CreatePhysicalEducationStr<br>ucture|Br, Structure, Classes|Skills / sub-skills|
|PET › Create Tests|/GradeBook/<br>PhysicalEducationTestCrea<br>tion|Br, Structure, Term 1–3|Get|
|PET › Tests Marks<br>Entry|/GradeBook/<br>PhysicalEducationTestMark<br>sEntry|Br, Cls, Sec, Part, Term|Get|
|PET › Report Cards|/GradeBook/<br>PhysicalEducationBulkRepo<br>rtCards|Br, Cls, Sec, Term,<br>Format 1–5+|Print|
|Reports › Health<br>Issues Observations|/Student/<br>StudentHealthIssueObserv|Br, Class type, Cls, Sec,<br>Observed at (School /|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,|
|---|---|---|---|
||||columns|
||ationsReport|Home / Hostel)||



### **IB, Cambridge and ICSE Gradebooks** 

These three boards share near-identical pages; only the endpoint suffix changes ( <mark>_IB</mark> , <mark>_Cambridge</mark> , <mark>_ICSE</mark> ). One Django gradebook app with a <mark>board</mark> field can serve all three. 

|Page|IB / Cambridge / ICSE endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Subjects (create)|/GradeBook/<br>CreateSubjectsEntryForIBBoard,<br>…ForCambridgeBoard, ICSE<br>equivalent|Branch type, Br,<br>Programme<br>(PYP/MYP/DP;<br>Primary / Lower /<br>Upper Sec / Advanced),<br>Board, Master subject,<br>Sub group, Name,<br>Code, Short code,<br>Description, Sequence,<br>Level (None / SL / HL),<br>Credits, Common /<br>Optional, Regional<br>language, Language<br>type, Block|Manage<br>languages,<br>optionals,<br>elective types,<br>subject blocks,<br>master subjects,<br>copy subjects,<br>branch subjects.<br>Cols: Name, No.<br>of mandatory<br>subjects, Is<br>language|
|IB Timetable (IB<br>only)|/Organisation/<br>FullTimeTableIBorCambridge|Br, AY|Tabs: Structure,<br>Schedule,<br>Subjects,<br>Co-/Extra-<br>curricular<br>periods,<br>Practical<br>batches|
|Homeroom Teacher<br>Remarks Master|/GradeBook/<br>ClassTeacherRemarksType(_Cam<br>bridge)|Br, AY|Get|
|Structure Creation|/GradeBook/CCEStructure_IB /<br>_Cambridge|AY, Br|Get|
|Manage<br>Examination<br>Scheme|/GradeBook/<br>ManageExaminationSchema_IB /<br>_Cambridge|AY, Br, Class, Subject<br>type|Get|



|Page|IB / Cambridge / ICSE endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Evaluation / Term<br>Report Card Publish<br>Settings|/GradeBook/<br>ParentReportCard(Evaluation)Se<br>ttings_IB / _Cambridge|Br, Class, Term,<br>Evaluation|Get|
|Manage Master<br>Examination<br>Scheme|/GradeBook/<br>ManageExaminationScheme_Mas<br>ter_IB / _Cambridge|Board, AY, Structure|Get|
|Attributes › Manage<br>Attribute<br>Statements (IB)|/GradeBook/ManageIBAttributes|Sequence, Statement|Default<br>statements.<br>Cols: Attribute,<br>Description,<br>Sequence,<br>Statement (IB<br>learner profile)|
|Attributes › Grading<br>Scale (IB)|/GradeBook/<br>CreateLearnerProfileGradingScale|Br, AY|Get|
|Attributes › Grade<br>Entry (IB)|/GradeBook/<br>ManageIBAttributesGradeEntry|Br, Class-Sec, Term|Get|
|ATL Skills › Grading<br>Scale (IB)|/GradeBook/<br>CreateATLSkillsGradingScale|Br, AY|Get|
|ATL Skills ›<br>Category / Cluster<br>Grade Entry (IB)|/GradeBook/<br>ManageIBATLSkillsGradeEntry|Br, Class-Sec, Term,<br>Category / Cluster<br>wise, Category|Get|
|Subject Outcomes,<br>Branch Specific,<br>Statements &<br>Grading Scale,<br>Grade Entry Status|…Strands_IB /_Cambridge,_<br>_BranchSpecificSubjectOutcomes,_<br>_AssignSubjectOutComeGradingSc_<br>_aletoClass__,<br>SubjectOutcomeGradeEntryStatu<br>s_*|As in CBSE; Cambridge<br>adds Grade type<br>(Scholastic / Effort)|Same|



### **Pre School** 

|Group › Page|Endpoint|Filters / inputs|Actions,<br>tabs,<br>columns|
|---|---|---|---|
|Curriculum › Classes|/GradeBook/PrePrimaryClasses|Board (Preschool, Early<br>Years, Montessori,<br>Kindergarten)|Add class,<br>class<br>categories|



|Group › Page|Endpoint|Filters / inputs|Actions,<br>tabs,<br>columns|
|---|---|---|---|
|Curriculum › Subjects|/GradeBook/<br>PrePrimaryCreateSubjectsEntry|Board, Programme,<br>Name, Code, Sequence|Save|
|Curriculum › Manage<br>Curriculum / Syllabus|/Communication/<br>LearningBasedAssessment_Curr<br>iculam|Br, Class type, Academic /<br>Non-academic|Get|
|Curriculum › Subject<br>Outcomes|/GradeBook/<br>SubjectStrands_Classes|Programme, Classes|Get|
|Curriculum › Subject<br>Outcome Grading Scale|/GradeBook/<br>CreateSubjectOutcomeGradingS<br>cale|Board, Default|Add /<br>import<br>scale. Cols:<br>Grade,<br>Point,<br>Remarks,<br>Icon|
|Curriculum › Statements<br>& Grading Scale|/GradeBook/<br>AssignSubjectOutComeGrading<br>ScaletoClass|(as CBSE)|—|
|LBA › Learning Based<br>Assessment|/GradeBook/<br>LearningAssessment|Br, Class type, Class,<br>Subject, Chapter, Class-<br>Sec, Term, Evaluation,<br>Strand|Outcome-<br>based<br>grade entry|
|LBA › Report Cards Bulk|/GradeBook/<br>LearningAssessmentReportCard<br>s|Br, Class-Sec, Subject,<br>Chapter, With / without<br>header, Status, Students|Get|
|LBA › Grading scale|/GradeBook/<br>LearningBasedAssessmentGradi<br>ngScale|Br, AY, Class type,<br>Classes; Grade, Point,<br>Colour code, Remarks|Add|
|Child Care › Manage<br>Daily Routines|/Organisation/<br>DailyLogForms_Main|Br, Class|Routine<br>templates<br>(meals,<br>nap…)|
|Child Care › Daily<br>Routine Entry|/Organisation/<br>DailyLogForms_Report|Br, Month, Cls, Sec|Get|
|Child Care › Class Room|/Connect/<br>ClassRoomActivityDetails_Lates|Br, Month, Cls, Sec|Get|



|Group › Page|Endpoint|Filters / inputs|Actions,<br>tabs,<br>columns|
|---|---|---|---|
|Activities|t|||
|Reports › Child Care Fee<br>Report|/FeeCollectionReports/<br>MonthWiseCollectionForChildC<br>areFee|AY, Br|6 tabs (as<br>Finance)|



### **Higher Ed (professional colleges)** 

Model: Programme Category › Programme / Department › Batch (regulation) › Programme Year › Semester › Course, with Course Outcomes (CO), Programme Outcomes (PO / graduate attributes), attainment and backlogs. 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Grade Book › Structure<br>Creation|/GradeBook/<br>CCEStructure_PU|AY, Br|Get|
|Grade Book › Create<br>Courses|/GradeBook/<br>CreateSubjectsEntryForHigh<br>erEd|Programme category,<br>Programme, Batch|Batches vs<br>Regulation,<br>Manage<br>curriculum<br>regulation,<br>Manage electives|
|Grade Book › Manage<br>Examination Scheme|/GradeBook/<br>ManageExaminationSchema<br>_HigherED|AY, Br, Programme,<br>Programme year, Course<br>type|Get|
|Grade Book ›<br>Evaluation / Term<br>Report Card Publish|/GradeBook/<br>ParentReportCard(Evaluatio<br>n)Settings_HigherED|Br, Programme year,<br>Semester, Evaluation|Get|
|Grade Book › Master<br>Examination Scheme|/GradeBook/<br>ManageExaminationScheme<br>_Master_HigherED|University, AY, Structure|Get|
|Grade Book › Student<br>Backlogs Report|/GradeBook/<br>RptStudentBacklogsReport|Br, Programme, Year,<br>Section|Get|
|Grade Book › Course<br>Assessment Tools|/Connect/<br>GradeBookAssessmentTools|Br, Programme|Get|
|Grade Book › Exam|/Connect/<br>StudentConsolidatedMarks_|Br, Programme, Year,<br>Section,Exam session,|Supplementary|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Marks Entry New|HigherED|Course|exam sessions|
|Grade Book › Course<br>Attainment<br>Percentages|/Connect/<br>CourseAttainmentPercentag<br>es|Br, AY, Programme, Year|Get|
|Outcomes › Course<br>Outcomes|/GradeBook/<br>CoCurricularSubjectStrands_<br>HigherEd|Programme category,<br>Course/Dept, Batch,<br>Year|Get|
|Outcomes ›<br>Statements & Grading<br>Scale|/GradeBook/<br>AssignSubjectOutComeGradi<br>ngScaletoClass_HigherED|Br, Programme category,<br>Course, Year, Scale<br>(marks or grade entry)|Grade<br>boundaries|
|Outcomes ›<br>Programme Outcomes|/ProfessionalStudent/<br>ManageProfessionalCollegeC<br>ourseOutcomes_Main|Programme category|Graduate<br>attributes|
|Outcomes ›<br>Programme<br>Departments|/Organisation/<br>ProgrammeDepartments|Br|Get|
|Outcomes › CO<br>Attainment Report|/GradeBook/<br>CourseOutComeAttainment<br>Report|Br, Programme, Year,<br>Semester, Internal<br>evaluation, Course, CO,<br>Format (detailed /<br>consolidated / question-<br>wise), from assessment /<br>Blooms levels|Get|
|Reports › Transcript|/Connect/<br>StudentTranscripts_HigherE<br>D|Br, Programme, Year,<br>Status, Student|Get|



### **Exam Cell** 

|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Before › Create Exam|/GradeBook/<br>HigherEdCreateExam|AY, Br, Programme,<br>Semester, Internal / External|Get|
|Before › Exam|/GradeBook/|AY, Br, Programme, Type|Tabs:|
|Timetable|RptHigherEdYearSemesterWi<br>seStudents||Programme<br>wise, Date|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||||wise|
|Before › Exam Room<br>Allocation|/GradeBook/<br>ManageExamRoomAllocatio<br>ns|AY, Br, Programme, Type,<br>Exam date, Exam time|Tabs: Room<br>allocation,<br>Seat<br>arrangement|
|Before › Invigilators<br>to Exam Rooms|/GradeBook/<br>AssignInvigilatorsToExamRoo<br>ms|Same|Get|
|Before › HallTicket<br>Numbers|/GradeBook/<br>RptHigherEdReferenceCodes|AY, Br, Programme year|Get|
|Before › Generate<br>Hall Tickets|/GradeBook/<br>PopulateHalltickets_HigherE<br>D|AY, Br, Programme, Year,<br>Term, Evaluation, show fee<br>due (none / balance / %),<br>with / without logo, per page,<br>photo, CBSE affiliation, org /<br>branch name|Get tests, Get<br>hall tickets|
|Before › Exam Fee<br>Paid Students|/GradeBook/<br>ExaminationFeePaidStudent<br>Report|AY, Br, Exam fee type, DR|Get|
|Before › Question<br>Paper Formats|/GradeBook/<br>QuestionPaperFormats_High<br>erED|Br, Programme, Year,<br>Semester, Evaluation, Course|Get|
|Before › OMR Sheet<br>Generation|/GradeBook/<br>StudentOMRSheetGeneratio<br>n|AY, Br, Type, Exam date,<br>Time, Course|Get, Print|
|During › Exam<br>Student Attendance|/GradeBook/<br>ExamRoomStudentAttendan<br>ce|AY, Br, Type, Date, Time,<br>Room|Get|
|During › Exam<br>Attendance Report|/GradeBook/<br>RptSubjectWiseExamRoomSt<br>udentAttendance|AY, Br, Programme, Type,<br>Date, Time|Get|
|During › Answer<br>Sheet Envelopes|/GradeBook/<br>AnswerSheetEnvelope|AY, Br, Type, Date, Time,<br>Room|Get|
|During › Envelope<br>Rack Management|/GradeBook/<br>AnswerSheetEnvelopeRackM|Same|Get|



|Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||anagement|||
|After › Question|/GradeBook/|Br, Programme, Year,|Get|
|Wise Marks Entry|QuestionPaperFormats_Mar<br>ksEntry_HigherED|Section, Semester,<br>Evaluation, Course, Test,<br>Student-wise / Answer-sheet-<br>wise||



### **LMS modules** 

|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Assignments ›<br>Assignment Grading<br>Scale|/Communication/<br>CreateAssignmentsGradin<br>gScale|Range from, Range to,<br>Grade|Default grades,<br>assign to<br>organisation|
|Assignments › Marks or<br>Grades visibility|/Communication/<br>AssignmentMarksOrGrad<br>esSettings|Per-branch Marks / Grades<br>toggles|Save|
|Assignments › Give<br>Assignments|/Organisation/<br>GiveAssignmentMDlevel|Br, Cls, Sec, Subject, DR,<br>Chapter, Topic|Assigned<br>students,<br>questions list,<br>edit<br>(coordinator /<br>principal<br>approval). Cols:<br>Class, Section,<br>Enrollment,<br>Student, Point<br>of contact,<br>Mobile|
|Assignments › Student<br>Online Assignments|/Organisation/<br>GetOnlineServiceAssigne<br>mnetData|AY, Br, Class type, Classes,<br>Sections, DR|Get|
|Assignments › Online<br>Assignments-Geneo|/Report/<br>GeneoAssessments|AY, Br, Class|Get|
|Assignments ›<br>Assignment Report|/Communication/<br>AssignmentReport_New|AY, Location, Br, Classes,<br>Sections, DR, Subject /<br>Teacher / Consolidated|Get|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|Assignments › Online<br>Assignment Status|/Communication/<br>OnlineAssignmentStatusR<br>eport|Location, Br, AY, Classes,<br>Sections, DR|Class-group-<br>wise status|
|Assignments › Online<br>Assignment Marks|/Communication/<br>OnlineAssignmentsClassW<br>iseReport|Class, Location, Br,<br>Subject, DR|Class-group-<br>wise marks|
|Online Classes › Enable /<br>Disable Access|/Student/<br>DeactiveStudentOnlineCla<br>sses|AY, Br, Class/Section|Get|
|Online Classes › SyncUp<br>Licenses|/Communication/<br>RptOnlineClassesLicences|—|Cols: Branch,<br>Parallel classes,<br>Expiry;<br>Recharge|
|Online Classes › Online<br>Classes|/Connect/<br>MCBOnlineClasses|Br|Create online<br>class|
|Online Classes › Online<br>Classes Report|/Communication/<br>RptOnlineClassesUsage|Br, AY, Report for, DR|Show|
|Content › Learning<br>(curriculum / syllabus)|/Subject/<br>LearningSubjects_New|Branch type, Br, Subject<br>type, Board, Class<br>programme, Programme<br>category, Course, Batch|Chapters /<br>topics /<br>content|
|Content › Branch<br>Content library|/Subject/<br>Branchwise_LearningSubj<br>ects|Same|Get|
|Content › Flash Cards|/Subject/<br>FlashCardSetsList|Br, Class|Create flash-<br>card sets|
|Content › Content<br>Resources|/Subject/<br>ContentResources|Branch, Class, Subject<br>pickers|Resources|
|Content › Question Bank|/Communication/<br>QuestionBankDashboard|Subject type, Branch type,<br>Board, Class programme,<br>Programme, Batch|Question<br>counts per<br>subject|
|Content › MCB Resources<br>LKG–V / VI–XII|/Communication/<br>PracticeQuestionsMainPa<br>ge,<br>/AssessmentLearningMai|—|Grade-wise<br>MCB question<br>banks|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||nPage|||
|Online Exams › Question<br>Bank|/Communication/<br>QuestionBankDashboard|(same)|—|
|Online Exams › Online<br>Exam / WorkSheet|/Student/<br>OnlineExamsDashboard|AY|Tabs: Objective<br>exams,<br>Summative /<br>Descriptive<br>exams|
|Online Exams › Allow<br>Multiple Attempts|/Organisation/<br>BranchSettingsAllowMulti<br>pleExamDuration|Per-branch toggle|Save|
|Online Exams › Delete<br>Online Exam Results|/Student/<br>OnlineExamsResultDeletio<br>n|Br, Class, Sec, Exam,<br>Search by|Search →<br>delete attempt|
|Online Exams › Exam Cell<br>(question paper)|/Examination/<br>CreateQuestionPaperMak<br>ingExams|Class, Subject, Manual /<br>Upload, Purpose (print /<br>online), Exam name,<br>Description, No. of<br>questions, Start date/time,<br>Duration, Max marks,<br>Blank pages, No. of parts|Add question<br>paper|
|Online Exams › Objective<br>Exam Analysis|/Report/<br>RptOnlineExamAnalysis|AY, Month|Dashboard|
|Online Exams ›<br>Summative Exam<br>Analysis|/Report/<br>SummativeExamsReport|Class, Section, Exam|Get|
|Baseline › Assign Baseline<br>Activity|/Student/<br>BaseLineActivityResults|Br, AY, Class, Term,<br>Evaluation, Master<br>category (General /<br>Sports / Medical)|Get|
|Baseline › Manage<br>Baseline Category|/Student/<br>ViewBaseLineCategory|AY, Board, Class category|List|
|Reflections › Create<br>Subject Reflections|/GradeBook/<br>SubjectWiseTeachersRefle<br>ctionTypes|Br, Board, Subject,<br>Chapter, Reflection,<br>Sequence, Month, Activity,<br>Strand,Outcome,|Grading scale,<br>Defaults|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
|||Materials, Activity<br>reflection||
|Subjects Mgmt ›<br>CBSE/State Subjects|/GradeBook/<br>CreateSubjectsEntry|Branch type, Board,<br>Programme, Course type,<br>Batch, Subject group, Sub<br>group, Master subject,<br>Name, Code, Short code,<br>Sequence, Academic /<br>Non-academic, Co- / Extra-<br>curricular, Discipline<br>subject, Include in CGPA,<br>Common / Optional,<br>Regional language|Languages,<br>optionals,<br>electives,<br>blocks,<br>additional<br>subject types,<br>master<br>subjects, copy,<br>branch subjects|
|Subjects Mgmt › IB /<br>Cambridge / ICSE /<br>Higher Ed Subjects|(same as gradebook<br>sections)|—|—|
|Subjects Mgmt › Grace<br>Marks Management|/GradeBook/<br>ClassWiseGraceMarksMa<br>nagement|AY, Board, Class<br>programme, Subject /<br>Subject-group wise|Get|
|Subjects Mgmt › Content<br>Planners (Org / Branch)|/GradeBook/<br>UnitPlannerUserManage<br>ment(_Branch)|Branch type, Board,<br>Programme, Class, Course,<br>Batch|Assign planners|
|Classroom Obs › Manage<br>Teacher observation|/Connect/<br>TeacherActivitesReport|Br, Month|Types: Teacher<br>observations,<br>Notebook<br>corrections,<br>Diary<br>maintenance,<br>Activities,<br>Syllabus<br>completion,<br>Co-scholastic,<br>Learning walk,<br>Short<br>walkthrough,<br>Clinical<br>observation,<br>School|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs,<br>columns|
|---|---|---|---|
||||ambience|
|Classroom Obs ›<br>Observations Report|/Connect/<br>RptAuditParametersRepor<br>t|AY, Br, Classes, Sections,<br>Staff, Observer, Status<br>(Under review /<br>Published / Read /<br>Responded…), Month /<br>DR, Format (2 detailed,<br>consolidated)|Get|
|Classroom Obs › Diary<br>Maintenance|/Staff/<br>TeacherObservationsDairy<br>Maintenance|Br, Teaching / Non-<br>teaching|List|
|Classroom Obs › Staff<br>Class Room Recordings|/Connect/<br>StaffClassRoomRecordings|AY, Br, Month|Get|
|Taxonomy › Create<br>Blooms Taxonomy Tests|/GradeBook/<br>BloomsTaxonomyTestCre<br>ation|Br|Get tests|
|Taxonomy › Questions /<br>Student Marks|/GradeBook/<br>GetClassGroupsForBloom<br>sTaxonomy|Br, Cls, Sec, Subject, Test|Get|
|Taxonomy › Blooms<br>Analysis Report|/GradeBook/<br>BloomsTaxonomyAnalysis<br>Report|Br, Class, Subject, Test|Get|
|Taxonomy › Chapter-wise<br>Diagnostic Assessment|/Connect/<br>SubjectLessonReflections<br>Assessment|Br, Board, Class,<br>Academic / Co-curricular|Get|
|Taxonomy › Diagnostic<br>Marks Entry|/Connect/<br>SubjectLessonReflections<br>Assessment_MarksEntry|Br, Cls, Sec, Subject, Type<br>(chapter end / topic / term<br>end), Chapter, Topic, Sort|Get|
|Taxonomy › Diagnostic<br>Analysis Report|/Connect/<br>ChapterwiseDiagnosticAss<br>essmentsAnalysisReport|Br, Class, Subject, Chapter|Get|
|Taxonomy › Score Card|/Connect/<br>ChapterWiseAssessmentR<br>eportCard|Br, Class-Sec, DR, Subject,<br>Tests, Status, Students|Print|
|Taxonomy › Topic-wise|/GradeBook/|(as Pre School LBA)|—|



|Module › Group › Page|Endpoint|Filters / inputs|Actions, tabs,|
|---|---|---|---|
||||columns|
|Learning Based|LearningAssessment|||
|Assessment||||



### **Locked add-ons (24) — from public sources** 

These modules aren't licensed for Alpha, so their screens can't be opened from this login. The specs below come from MyClassboard's public knowledge base and product pages. Where the vendor says little, the scope is filled with standard school-ERP practice and marked "proposed". Treat them as design targets, not a copy. 

|Suite › Add-on|What MCB documents|Proposed screens / data for Django|
|---|---|---|
|HR › Payroll<br>(HR Plus)|Payroll month settings; Payroll Entity (per<br>branch, linked to fee account); Staff Pay<br>Types; Add Allowances / Deductions<br>(HRA, DA, PF, ESI…); Basic salary settings<br>(Manual or % of gross); Staff salary<br>details; Upload staff allowances (CSV by<br>branch, department, month); Staff<br>taxable earnings; Staff advances;<br>Generate salary wizard (Start → Final<br>review → Confirm); Staff pay register;<br>Salary statements; PF details; ESI;<br>Download / email payslips; TDS report;<br>MIS report; PF report|SalaryComponent (earning/deduction,<br>fixed / % / formula, taxable),<br>SalaryStructure per staff, PayrollMonth<br>(attendance-linked LOP), PayrollRun,<br>Payslip + lines, Advance / Loan with<br>EMI, statutory (PF, ESI, PT, TDS) reports,<br>bank transfer file|
|HR ›<br>Recruitment|Accept Recruitments (search by<br>recruitment code, fill mandatory fields,<br>approve); Recruitment staff approval;<br>Appointment letter; Recruitment exam<br>report; Resignation approvals|JobOpening, Applicant (public apply<br>form), interview / exam rounds and<br>scores, offer and appointment letter<br>template, convert to Staff|
|HR › PMS (Staff<br>Assessment)|Create assessment (name, description,<br>General / Academic); Objectives (name,<br>description, weightage) › Indicators;<br>Grading scale (grade, point, remarks);<br>Assessment levels (sequence, name,<br>assessed by, confidentiality: next level /<br>everyone / none, sequential / parallel);<br>designation tiers; Take assessment<br>(teacher, subject, grade per indicator,<br>comments, overall feedback); Reports<br>Format 1(weighted byobjective)and|Assessment, Objective, Indicator,<br>GradeScale, AssessmentLevel,<br>AssessmentEntry, AssessmentScore;<br>workflow Self → Peer → Coordinator →<br>HOD → HM → Principal|



|Suite › Add-on|What MCB documents|Proposed screens / data for Django|
|---|---|---|
||Format 2 (indicator grades)||
|HR ›<br>Continuous<br>Professional<br>Development|Not documented (proposed)|PD programme catalogue, staff<br>enrolment, hours / credits, certificates,<br>PD log (already partly in HR › Staff<br>Trainings & PD)|
|ERP › Visitor<br>Management|Visitor details; Parent visitor slip (class,<br>section, student); Outside visitor slip with<br>OTP and mobile-app approval; Gate pass:<br>student and staff, update exit / in time;<br>date- and month-wise reports;<br>dashboard with monthly counts|Visitor, Visit (purpose, host, photo, ID,<br>OTP, in/out time, badge), GatePass<br>(student/staff, reason, approver,<br>out/in), reports|
|ERP › Mobile<br>Apps|Parent app (dashboard, sibling accounts<br>linked by mobile number, diary,<br>attendance, fees, notices); Teacher app<br>(diary, assignments, attendance, events,<br>photos, notices); Smart School admin<br>app; Pre-admission app (data collection,<br>document upload, application)|Django REST / DRF APIs + JWT for each<br>app; menus are already configurable in<br>Organisation › Manage Menus|
|ERP ›<br>Franchisee|AESC (authorised study centre) settings;<br>dealer / vendor settings; multi-location<br>oversight|Franchise, Centre, royalty / fee share,<br>centre-wise reports|
|ERP ›<br>Placements|Not documented (proposed)|Company, Drive, eligibility rules, student<br>applications, rounds, offers, placement<br>statistics|
|ERP › Student<br>Council|Manage elections (register candidates);<br>cycle of planning, announcements,<br>voting, results|Council posts, Election, Nomination,<br>Vote (one per eligible voter), Result,<br>tenure|
|ERP › Infirmary|Student health infirmary records;<br>medical records and services for students<br>and staff|InfirmaryVisit (complaint, vitals,<br>treatment, medicine issued, sent<br>home / parent informed), medicine<br>stock, health incidents (links to ECA ›<br>Student Health Details)|
|ERP › RFID|Access control and asset tracking; RFID<br>attendance (MCB already has RFID data-<br>log pages)|Card issue, reader devices, punch log<br>ingestion API, gate / bus / campus<br>attendance|
|ERP ›|Not documented (proposed)|Audit checklist templates, audit visits,|
|Academic||scores,action items(related to Class|



|Suite › Add-on|What MCB documents|Proposed screens / data for Django|
|---|---|---|
|Audit||Room Observation)|
|Finance ›<br>School Services|Centralised access to school services<br>(proposed: paid services such as clubs,<br>coaching, day care)|Service catalogue, subscription per<br>student, billing into fee module|
|Finance › PDC<br>Management|Record post-dated cheques; deposits,<br>clearances, summaries|PDC (student, cheque no, bank, date,<br>amount, installment), deposit batch,<br>clearance / bounce status, reminders|
|CRM ›<br>Admissions<br>Plus CRM|Unified inquiry-to-enrollment CRM; lead<br>management, lead nurturing, campaigns;<br>LeadSquared / Meritto integrations|Lead scoring, pipeline board, task /<br>follow-up automation, call logging,<br>campaign attribution (extends the<br>Admissions module)|
|CRM ›<br>WhatsApp<br>Marketing|WhatsApp business marketing for<br>admissions|Broadcast campaigns to leads, template<br>approval, opt-in, click / reply tracking|
|Add-on ›<br>Alumni<br>Management|Manage ex-student data|Alumni profile (batch, higher studies,<br>job), events, donations, directory,<br>alumni portal login|
|Add-on › SQAA|CBSE School Quality Assessment &<br>Assurance|SQAA domains and standards, evidence<br>upload, self-assessment scores, reports|
|Add-on ›<br>Automated<br>Alerts|Organisation-wide automatic alerts in<br>real time|Rule engine: event (absent, fee due,<br>birthday, low attendance…) → channel<br>(SMS / WhatsApp / push / email) →<br>schedule (Celery beat)|
|Add-on › NAAC<br>and NIRF|Not documented (proposed)|Criteria-wise data templates (NAAC 7<br>criteria, NIRF parameters), evidence<br>files, SSR export|
|Add-on ›<br>Digital<br>Document<br>Library|Not documented in detail (proposed)|Organisation document repository with<br>folders, versioning, access control|
|Gradebook › AI<br>Exam Cell|AI question paper generator|Blueprint (chapters, Blooms level,<br>marks) → generate paper from question<br>bank / LLM, answer key|
|LMS › JEE<br>MAINS|Not documented (proposed)|JEE practice tests, NTA-style scoring,<br>rank prediction|
|LMS › G Suite|Google Workspace/Meet integration|Google OAuth,Classroom/Meet links|



|Suite › Add-on|What MCB documents|Proposed screens / data for Django|
|---|---|---|
|||on timetable periods|



## **Observations for the Django build** 

About 70% of MCB's 855 menu pages are filter-then-report screens built on the same five filters, so a generic report framework will cover most of the scope. 

#### **Shared building blocks to build once** 

1. Global context: Organisation › Location/Zone › Branch, plus Academic Year and Financial Year selectors. Nearly every page filters by AY + Branch; keep them in the session/header like MCB's AY chip. 

2. Common filter set: AY, Branch, Class, Section, Status (Active / Inactive / Both), Department, and a date-range widget (Today / 7 / 30 days / Date range / Till date). One reusable <mark>ReportFilterForm</mark> + Select2 widgets. 

3. Report engine: filter form → queryset → table with Add/Remove Columns, Consolidated / Detailed toggle, export to Excel / CSV / PDF / Print. Many MCB reports are just tab variants of one query. 

4. Student search widget: search by Name / Enrollment Code / Admission No / Application No / Father mobile / Transaction ID; reused by certificates, fee edits, store, hostel, TC. 

5. Approval workflow engine: concession, fee unassign, payment change, refund (Principal → Accounts), inactive / reactive student, staff inactivation, leaves (3 reporting levels), diary, announcements, photo gallery, purchase / contracts, petty cash. One <mark>ApprovalRequest</mark> model with type, level and status. 

6. Template-based messaging hub: one template table and one send-log for SMS (DLT), WhatsApp (BSP templates, 24-hour reply window), Email, Voice and App push. Every module's "send" page is the same recipient picker (Point of contact / Father / Mother / Student) + template + preview. 

7. Document designer: certificates, TC, bonafide, ID cards (student / staff / APAAR), report cards, fee receipts and reminder slips all use template + bulk print layout (cards per row, rows per page, spacing, width/height). 

8. Upload / import pattern: download format → validate → show correct / incorrect / duplicate counts → error file → commit (enquiries, applications, fee receivables, concessions, petty cash, timetable, biometric, measurements). 

9. Audit logs: data-change logs for students, staff, fees, fines, due dates and report downloads. 

**Suggested Django apps** (mapping MCB modules) 

|Django app|MCB modules covered|
|---|---|
|core (org, branch, AY, users, roles, menus)|Organisation, Login Statistics, Manage Menus|
|students|SIS, Learner Profile, Achievements, Mentors,<br>ii|
||Certificates|
|admissions|Admissions (CRM), Dynamic / public forms|



|Django app|MCB modules covered|
|---|---|
|fees|Finance, Finance Intelligence, Scholarship|
|accounts|Expenses Management|
|hr|HR, Staff Wall, staff tasks, biometric|
|transport|Transport, VTS|
|hostel|Hostel, Meals|
|inventory / store|Inventory, School Store|
|library|Library|
|helpdesk|Concerns, TC requests|
|comms|SMS, WhatsApp, Email, Voice, Notifications, Diary,<br>Announcements, Calendar, Gallery, Student Wall|
|gradebook|CBSE/State, IB, Cambridge, ICSE, Higher Ed, Pre<br>School, ECA/PET, Exam Cell|
|lms|Assignments, Online Classes, Content, Online<br>Exams, Baseline, Reflections, Subjects, Classroom<br>Observation, Learning Taxonomy|



#### **Notable MCB details** 

- Duplicate pages appear under several menus (e.g. Fee Transaction Summary, Admission Details Report, Student Strength, Inactive Students, Staff Kids report). Build each once and link it from several menus. 

- Hostel › Reports › Warden Details is broken in MCB (redirects to an error page). 

- Locked add-ons not analysed: Payroll, PMS, Recruitment, CPD, Visitor Mgmt, Mobile Apps, Franchisee, Placements, Student Council, Infirmary, RFID, Academic Audit, School Services, PDC Management, Admissions Plus CRM, WhatsApp Marketing, Alumni, SQAA, Automated Alerts, NAAC/NIRF, Digital Document Library, AI Exam Cell, JEE Mains, G Suite. 

- Several pages are only filter shells; their result grids and form fields load by AJAX after Get, so columns are listed only where the server returned them. 

## **Django data model — all modules** 

The plan has 16 Django apps covering all 71 modules, with about 230 models. Conventions: every business model inherits <mark>TenantModel</mark> (organisation FK, created/updated by and at, is_active). Yearscoped models also carry <mark>academic_year</mark> and <mark>branch</mark> . Choices use <mark>TextChoices</mark> , and money uses <mark>DecimalField(12, 2)</mark> . 

**core — organisation, users, access** 

|Model|Key fields|
|---|---|
|Organisation|name, code, logo, school_code, edition, login_url,<br>sms_sender_id|
|Location (Zone)|organisation, name|
|Branch|location, name, short_code, branch_type (School /<br>College / Preschool / Junior College), board(s),<br>state, city, address, logo, enrollment_prefix,<br>sms_sender_id, receipt_type, has_biometric,<br>has_vts, is_revenue_branch|
|AcademicYear|name (2026-2027), start, end, is_current,<br>is_preadmission; months (AcademicMonth)|
|FinancialYear|name, start, end|
|Board|name (CBSE, State, IB, Cambridge, ICSE, Preschool,<br>University)|
|ClassCategory / Programme|board, name (Pre-primary, Primary, PYP, MYP, DP,<br>UG…)|
|Class (Grade)|category, name, sequence, stream (Science /<br>Commerce)|
|Section|branch, class, academic_year, name, capacity,<br>class_teachers (M2M Staff), is_holding (New<br>Admission)|
|House / ClassGroup|branch, AY, name, group_type (Academic, House,<br>Practical, Finance, Store, Custom, Club, ECA,<br>Project, Tag, Segment)|
|User (AbstractUser)|user_type (Admin, Staff, Student, Parent), mobile,<br>alias_username, mpin, two_factor_method|
|AccessLevel|Organisation / Zonal / Branch / Staff / Class<br>teacher|
|Role, RoleMenu|role, module, menu_item,<br>can_view/add/edit/delete/approve|
|Module, MenuGroup, MenuItem|code, name, suite, is_locked, url_name, sequence<br>(drives the module switcher and menus)|
|UserBranchAccess|user, branch(es)|
|LoginLog,AuditLog,ReportDownloadLog|user,ip,action,model,object_id,diff JSON,filters|



|Model|Key fields|
|---|---|
||JSON|
|Setting|scope (org/branch), key, value JSON (password<br>rules, OTP, chat settings…)|
|Feedback, SupportTicket, FAQ|—|



### **students — SIS, learner profile, certificates** 

|Model|Key fields|
|---|---|
|Student|enrollment_code, admission_no, gr_no, roll_no,<br>first/middle/last name, gender, dob, doa, email,<br>mobile, photo, blood_group, religion, caste,<br>sub_caste, mother_tongue, nationality, citizenship,<br>aadhaar, pen, apaar_id, smart_card_no,<br>unique_code(+dates), state_govt_no,<br>place_of_birth(+village, district, state, country),<br>identification_marks, previous_school, quota,<br>regular/lateral, admission_category (Day /<br>Residential…), segment, scholarship_eligible, status<br>(Active / Inactive / Suspended / Alumni / TC)|
|StudentEnrollment|student, academic_year, branch, class, section,<br>roll_no, house, is_promoted, promoted_from (yearly<br>placement)|
|Parent|student(s) M2M via ParentLink (relation Father /<br>Mother / Guardian), name, mobile, email, alt_email,<br>qualification, occupation, company, designation,<br>aadhaar, pan, dob, nationality, blood_group, pen,<br>passport/visa, annual_income, photo|
|StudentFamily|parental_status, custodian, point_of_contact,<br>marriage_anniversary, family_id|
|Sibling|student, sibling_student (or external name, code,<br>occupation, mobile)|
|Address|student, type (current / permanent), address,<br>locality, city, state, country, pin, lat, lng|
|IdentityDocument|person (generic FK), passport_no, issue place/date,<br>validity, visa_no, issue/expiry|
|StudentDocument|student, doc_type, status (Yes / No / NA), file,|



|Model|Key fields|
|---|---|
||verified_by|
|StudentStatusRequest|student, type (inactivate / reactivate / suspend),<br>reason, effective date, approval FK|
|BranchTransfer|student, from/to branch/class/section, AY|
|Promotion|student, from AY/class, to AY/class, result|
|Attendance (StudentAttendance)|student, date, session / period, status (P/A/L/Leave),<br>source (manual / biometric / RFID / transport),<br>marked_by|
|LeaveIntimation|student, from, to, type, reason|
|Timetable models|Period, TimetableStructure, TimetableSlot (section,<br>day, period, subject, staff), Substitution,<br>PracticalBatch|
|DisciplineCategory / DisciplineEntry|category, sub-category, negative marks, severity,<br>form_type (normal / anti-bullying); entry: student,<br>staff, date, remarks|
|AnecdoteType / Anecdote|type (appreciation / needs work), badges, icon, notify<br>flags|
|Observation|student, staff, area, text, date|
|Achievement|scope (institute / student / staff), category, sub-<br>category, level, event, venue, city, dates, result|
|Mentor|staff, students M2M|
|CertificateType / CertificateTemplate|type (Bonafide, Study, TC, DOB, Conduct, Income tax,<br>Deposit, No Due, Promotion, Achievement…), HTML<br>template with merge fields, numbering series per<br>branch|
|IssuedCertificate|student, type, number, data JSON, issued_on,<br>issued_by|
|TransferCertificate|student, tc_no, reason, leaving date, conduct,<br>fee_clearance, issued|
|IDCardTemplate / IDCardPrintJob|type (student / staff / APAAR), layout (width, height,<br>per row, rows)|



### **admissions — CRM, forms** 

|Model|Key fields|
|---|---|
|Source / Campaign|name, type (walk-in, website, Google, Meta, referral<br>types), cost|
|Lead|name, mobile, email, source, campaign, branch,<br>assigned_to, status|
|Enquiry|AY, branch, admission_type, class_sought, student<br>name, dob, gender, parent name, mobile, email,<br>source, counsellor, stage (Open, Closed, Application<br>stage/taken/cancelled…), country, sibling_ref,<br>referral|
|FollowUp|enquiry, date, mode (call / visit / WhatsApp),<br>remarks, next_followup_on, by|
|ParentVisit / WalkinSurvey|enquiry, scheduled, completed, answers JSON|
|Application (Registration)|enquiry, application_no, form data JSON, fee_paid,<br>receipt, status|
|EntranceExam / ExamResult|class, subjects, marks|
|SelectionApproval|application, remarks_type, status|
|Admission|application, student (created), class, section,<br>admission_type, fee_plan, concession_request, date|
|AdmissionCancellation|admission, reason, refund|
|OnlineLink|type (registration / admission), recipient, sent_at|
|MandatoryField|branch,class,fieldname|
|DynamicForm / DynamicField /<br>DynamicResponse / DynamicAnswer|i_<br>form: type (student / staff / public / correction /<br>next-AY / transport), scope, last_date, fee link; field:<br>17 types, options, merge_key|
|Target|branch, class, AY, target_strength|



**fees — finance** 

|Model|Key fields|
|---|---|
|FeeAccount|branch, name, receipt_prefix, bank account, gst_no|
|FeeType|name, category (Regular / Misc / Transport /<br>Application / Registration / Exam / Hostel /|
||i  i<br>Deposit/Daycare/Lunch/Enrichment),|



|Model|Key fields|
|---|---|
||occurrence (one-time / installment / monthly /<br>service-based), refundable, taxable + SAC/GST|
|FeePlan|AY, branch, fee_type, name, classes M2M,<br>student_type (New / Existing / Both), route slab<br>(transport), total|
|Installment|fee_plan, name, due_date, amount, sequence|
|StudentFee (Receivable)|student, AY, fee_plan, installment, amount,<br>concession, net, paid, balance, due_date|
|Concession / ConcessionType|type (staff kid, sibling, merit, early-bird,<br>management), student_fee, amount or %, approval<br>FK|
|Scholarship / ScholarshipAssignment /<br>Disbursement|—|
|FineRule|fee_type, installment, per_day / slab, grace_days,<br>max|
|Receipt (Payment)|receipt_no, student, fee_account, date, mode (Cash,<br>Cheque, DD, Card, UPI, Online PG, ECS), amount,<br>bank/cheque details, status (Active / Cancelled /<br>Bounced), source (counter / online / app)|
|ReceiptLine|receipt, student_fee, amount, fine|
|Cheque|receipt, cheque_no, bank, date, deposit_date,<br>deposited_account, cleared_on, bounced_on,<br>bounce_charge|
|OnlineTransaction|gateway, txn_id, order_id, status, payload JSON,<br>device|
|Invoice / Challan|student, period, lines, due|
|Refund|student, receipt, amount, reason, approval steps,<br>paid_by, mode|
|CreditNote / Wallet / Advance|student, amount, balance|
|FeeChangeRequest|type (unassign, amount change, date change,<br>receipt change, cancel), approval FK|
|LastYearDue|student, from_AY, to_AY, amount|
|CollectionFollowUp|student, date, remarks, next date, by|



|Model|Key fields|
|---|---|
|BankReconciliation|account, statement line, receipt match|
|GSTSetting, SACCode|—|



### **accounts — expenses, petty cash, ledgers** 

|Model|Key fields|
|---|---|
|LedgerGroup / Ledger (Chart of accounts)|type (Income, Expense, Liability, Asset, Other),<br>parent, branch|
|Party|name, type (vendor / staff / other), bank|
|BankAccount / CashAccount|branch, name, opening balance|
|Voucher|type (Payment, Receipt, Journal, Contra / Transfer,<br>Petty cash withdrawal, Cash deposit), date, FY,<br>narration, approval FK|
|VoucherLine|voucher, ledger, debit, credit, party, bus_no (for<br>transport costs)|
|PeriodicBill|branch, ledger, frequency, amount (regular<br>maintenance)|
|Reports|Day sheet, Ledger, Trial balance, Income &<br>Expense, Balance sheet, Final account, Cash/Bank<br>balances (queries over VoucherLine + fee Receipts)|



### **hr — staff, attendance, leave, tasks, payroll** 

|Model|Key fields|
|---|---|
|Department, Designation (tier), Qualification|—|
|Staff|user, staff_code, ref_code, biometric_code, type<br>(Teaching / Non-teaching / Transport / Outsource),<br>department, designation, branch(es),<br>first/middle/last, dob, gender, married,<br>qualification, B.Ed / M.Ed, specialisation, CTET +<br>score, trained_as, subjects, contact fields, address,<br>bank, EPF / UAN / ESI, insurance, licence, passport,<br>govt id, aadhaar, pan, blood group, height, weight,<br>disabilities, doj, payroll_entity, payment_type,<br>salary_type, status, inactive_reason|
|StaffFamily, StaffDocument, StaffRemark,|—|



|Model|Key fields|
|---|---|
|StaffNOC, StaffExit||
|ReportingLevel|staff, level (1–3), reports_to|
|Shift / Session / WeeklyOff|branch, type (time-based / work-hours), in/out,<br>grace, half-day rules|
|StaffAttendance|staff, date, session, status, in/out time, source<br>(manual / biometric / RFID / FR / GPS / WFH), late /<br>early flags|
|BiometricPunch|device_id, code, timestamp (raw device log)|
|AttendanceModification / Regularization|staff, date, from → to, reason, approval FK|
|WorkFromHome|staff, from, to|
|LeaveType / LeaveCategory / LeavePolicy|paid / unpaid, credit per month, carry forward,<br>department mapping|
|LeaveBalance / LeaveApplication|staff, type, from, to, half_day, status, approval chain|
|Holiday / LeaveWindow|branch, category, dates, optional|
|CompOff / PermissionRequest|—|
|StaffTask (designation task template) /<br>TaskAssignment / TaskSubmission|frequency (daily / weekly / monthly / yearly), due,<br>status|
|StaffFeedback (praise / complaint / note)|staff, by, type, text|
|TrainingPD|staff, type (training, PD, achievement, research),<br>hours, certificate|
|StaffGroup|custom / system, members|
|StaffWallPost / StaffMeeting|group, topic, attachment, comments, emergency<br>flag; meeting: online / face-to-face, schedule|
|Payroll (add-on)|PayrollEntity, SalaryComponent, SalaryStructure,<br>PayrollMonth, PayrollRun, Payslip, PayslipLine,<br>StaffAdvance|
|Recruitment (add-on)|JobOpening, Applicant, InterviewRound, Offer|
|PMS (add-on)|Assessment, Objective, Indicator, AssessmentLevel,<br>AssessmentEntry|



### **transport** 

|Model|Key fields|
|---|---|
|Vehicle|branch(es), reg_no, type, seating capacity, vts_vendor,<br>gps_device_id, fitness / insurance / permit expiry|
|Driver / Attender (transport staff)|staff FK, licence|
|Route|AY, branch, name, vehicle, driver, attender, type<br>(pickup / drop / both)|
|Stop|route, name, sequence, lat, lng, pickup_time, drop_time,<br>distance_km, fee_slab|
|Zone / Locality|branch, name, polygon|
|StudentTransport|student, AY, pickup_route, pickup_stop, drop_route,<br>drop_stop, fee_plan, from_date, to_date|
|TransportAttendance|student, date, trip (pickup / drop), status, source (RFID /<br>app)|
|VehicleLog|vehicle, date, type (fuel / maintenance / breakdown),<br>litres, km, cost|
|VTSVendor / VTSSetting|branch, vendor, username, password (encrypted), url|
|Trip / LiveLocation|vehicle, start, end; lat, lng, ts (cache, not DB, if real-time)|



### **hostel** 

|Model|Key fields|
|---|---|
|HostelBuilding › Floor › Room › Bed|branch(es) M2M, gender, capacity|
|HostelAdmission|student, AY, bed, category (Residential / Semi / AC),<br>from, to|
|HostelAttendance|student, date, status, remark|
|HostelLeave / GatePass|student, type, from, to, approved_by, out_time,<br>in_time|
|Warden|staff, building|
|HostelDepositCategory / HostelDeposit /<br>HostelTransaction|category (Dhobi, Medical, Misc…), collection<br>account, min deposit, student wallet ledger|
|ItemCategory / Item / DailyPurchase /<br>DailyConsumption|category (provisions, vegetables, housekeeping, gas,<br>electrical), UOM, vendor, qty, cost|
|MealSeason/Meal/MealMenu/|weekday,meal,items,time|



|Model|Key fields|
|---|---|
|MealSchedule||
|Committee / CommitteeTask|head, members, task, accomplished, status|
|HostelAnnouncement, ItemsToBring,|—|
|WardenRemark||



### **inventory and store** 

|Model|Key fields|
|---|---|
|Store|branch(es), incharge, signatures|
|ItemCategory › SubCategory › ItemType › Item|HSN, GST %, UOM, is_fixed_asset, is_returnable,<br>barcode|
|StockLedger|store / branch, item, date, txn_type (inward,<br>outward, transfer, issue, sale, damage, return), qty,<br>rate, ref|
|Vendor|code, name, contact, PAN, GSTIN, MSME, bank,<br>services (sales / AMC / outsource), verified,<br>documents|
|RFQ / Quotation / PurchaseOrder / POLine /<br>GRN (Stock Invoice Inward)|PO no, dates, vendor, challan, invoice|
|Contract|type (service, rate, AMC, manpower, work order),<br>vendor, period, value, approval chain|
|Asset|item, type (fixed, current, tangible, intangible,<br>financial, consumable), location, purchase,<br>depreciation|
|StaffIssue / StudentIssue|item, qty, issued_on, returnable, returned_on|
|SchoolStore|name, GSTIN, delivery_by, delivery_vendor,<br>fee_account, payment gateway, partial payment,<br>individual sale|
|StoreCategory › StoreItemCategory › StoreItem<br>(SKU, size, price, vendor)|—|
|Kit / KitItem|class or house, AY, store, individual-sale flag|
|StudentStoreAssignment|student, item / kit, qty|
|StoreOrder / StoreOrderLine|student, store, payment (online / COD / pay at|



|Model|Key fields|
|---|---|
||school), status, delivery status, delivered_on|
|SizeMeasurement|student, AY, type (uniform / shoe), sizes JSON, unit|



### **library** 

|Model|Key fields|
|---|---|
|Library|branch, name, librarians, default search|
|CategoryType, Category, SubCategory,<br>Publisher, Vendor, Language|—|
|Book (title record)|title, author(s), ISBN / ISSN, publisher, category,<br>language, edition, price, specimen|
|BookCopy|book, access_no, barcode, library, status (available,<br>issued, lost, damaged), purchase date|
|Issue|copy, borrower (student / staff), issued_on, due_on,<br>returned_on, fine|
|LibraryRule|branch, user_type, max_books, return_days, late<br>fine / day, damage %, lost %|
|DigitalBook|title, ref_code, language, url / file, classes M2M|
|LexileScale / ReaderAssessment|grade ranges, parameters, term scores|
|LibraryUsageLog|user, in/out time|



### **helpdesk — concerns and TC requests** 

|Model|Key fields|
|---|---|
|ConcernCategory / ConcernType|audience (parent / staff / branch), category, description,<br>notice period, escalate L2 / L3 days, response / resolution<br>target hours, indent flag|
|ConcernAssignee|type, branch, level, user|
|Concern (Ticket)|ref_no, type, raised_by, student / staff, message,<br>attachments, status, level, due_at|
|ConcernComment / StatusLog|—|
|TCRequest|student, reason, stage (class teacher → coordinator →<br>principal → accounts), counselling notes, fee<br>(processing / notice period), status|



|Model|Key fields|
|---|---|
|AgingSetting|branch, days|



**comms — SMS, WhatsApp, email, voice, push, diary, announcements, calendar, gallery, walls** 

|Model|Key fields|
|---|---|
|Channel / ProviderConfig|channel (SMS, WhatsApp, Email, Voice, Push),<br>provider (DLT gateway, AiSensy / BSP, SMTP,<br>Kaleyra, FCM / Ably), credentials (encrypted),<br>sender IDs, DLT entity / header IDs|
|MessageTemplate|channel, module, name, body with placeholders,<br>DLT template ID / WhatsApp template name, media<br>type, status (approved)|
|CreditWallet / Recharge|channel, balance, plan, txn|
|MessageJob|channel, template, audience filter JSON (branch,<br>class, section, group, segment, route, status),<br>recipient type (POC / father / mother / student /<br>staff), scheduled_at, created_by|
|MessageRecipient (Log)|job, person, number / email / device, rendered text,<br>provider_msg_id, status (queued, sent, delivered,<br>failed, read), error|
|IncomingMessage|channel, from, text, linked student, replied_by,<br>replied_at (WhatsApp two-way)|
|OptIn|person, channel, status|
|DiaryEntry|section, subject, date, text, attachments, staff,<br>approval status|
|AnnouncementType / Announcement|type flags (branch-level, subject, circular, staff,<br>approval), title, body, audience, display dates, scroll,<br>attachments, via email / WhatsApp|
|CalendarEvent / EventType / Vacation /<br>Holiday|scope (school / class / exam), dates|
|ActivityAlbum / Photo|type (general, subject, house, club, ECA, event),<br>class, approval|
|ChatGroup / ChatMessage (Student wall, Class<br>wall)|group (class / subject), sender, text, tag, replied|
|AutomatedAlertRule (add-on)|event, channel, template, schedule|



|Model|Key fields|
|---|---|
|GreetingTemplate|occasion (birthdays, anniversaries), image|
|ClickToCallAgent / CallLog|agent, number, call type, duration, recording|



### **gradebook — CBSE / State, IB, Cambridge, ICSE, Higher Ed, Pre-school, ECA / PET, exam cell** 

|Model|Key fields|
|---|---|
|Subject|board, class category, group, master subject, name,<br>code, short code, sequence, academic / non-<br>academic, co / extra-curricular, discipline,<br>include_in_cgpa, common / optional / elective /<br>language, level (SL / HL), credits, block|
|ClassSubject / StudentSubject|section / student, subject (optional & language<br>choices)|
|Structure|AY, branch, board, name; Part (scholastic / co-<br>scholastic)|
|Term › Evaluation › ExamType|structure, name, sequence, weightage|
|Test|section / class, subject, evaluation, exam_type,<br>max_marks, date, is_grade_entry|
|Mark|test, student, marks / grade, absent, remarks|
|GradingScale / Grade|name, type (marks / grade / effort), grade, point,<br>from–to %, remarks, icon, colour|
|ExamScheme (report-card logic)|structure, class, formula JSON (best of, average,<br>weightage, rounding), rank rules|
|ComputedResult|student, term / evaluation, subject totals, %, grade,<br>rank (posted by "Update results")|
|Skill / SkillGrade|co-scholastic skills per subject / part|
|RemarkIndicator / StudentRemark|category, grade, statement; class teacher / subject<br>remarks|
|SubjectOutcome (Strand) / OutcomeStatement<br>/ OutcomeGrade|board, class, subject, strand, statement, grade per<br>student|
|IBAttribute / ATLSkill (+ grades)|IB learner profile and ATL clusters|
|ReportCardTemplate / ReportCardPublish|type (term / evaluation), template, publish date,<br>reopen date, enabled for parents|



|Model|Key fields|
|---|---|
|OtherExam / CompetitiveExam / HallTicket|name, classes, month, grading; competitive exam<br>fee|
|ECAActivity / PETStructure / PETTest /<br>PETMark / HealthRecord|indoor / outdoor, stages, height, weight, BMI,<br>CWSN, observations|
|PreschoolCurriculum / LBAOutcome /<br>LBAGrade / DailyRoutine / RoutineEntry|Montessori / LBA grading with colour codes; daily<br>logs|
|HigherEd: Programme, Batch (regulation),<br>ProgrammeYear, Semester, Course, Elective,<br>CourseOutcome (CO), ProgrammeOutcome<br>(PO), COPOMap, AttainmentTarget,<br>AssessmentTool, Backlog,<br>SupplementarySession, Transcript|—|
|ExamCell: Exam, ExamTimetable, ExamRoom,<br>SeatAllocation, Invigilator, HallTicketNumber,<br>QuestionPaperFormat, OMRSheet,<br>ExamAttendance, AnswerSheetEnvelope,<br>RackLocation, QuestionMark|internal / external, date, time, room, seat|
|GraceMark|AY, board, class, subject / group, marks|



**lms — assignments, content, online exams, classes, observation, taxonomy** 

|Model|Key fields|
|---|---|
|Chapter › Topic › LearningResource|subject, class, board; resource type (video, pdf, link,<br>flash card), branch-level library|
|ContentPlanner (unit plan)|org / branch level, class, subject, chapter, assigned<br>users|
|Assignment / AssignmentSubmission|section, subject, chapter, topic, due, attachments,<br>online questions, marks / grade, visibility setting,<br>approval|
|AssignmentGradeScale|from, to, grade|
|Question (bank)|subject, chapter, topic, type (MCQ, multi, fill,<br>descriptive), Blooms level, difficulty, options JSON,<br>answer, marks|
|OnlineExam / ExamQuestion / Attempt /<br>AttemptAnswer|objective / summative, schedule, duration, multiple<br>attempts, shuffle, auto-grade|
|QuestionPaper|class,subject,manual / upload, purpose(print /|



|Model|Key fields|
|---|---|
||online), parts, marks|
|OnlineClass / Licence|provider (SyncUp, Zoom, Meet), section, subject,<br>schedule, link, attendance|
|BaselineCategory / BaselineResult|general / sports / medical|
|SubjectReflection / ActivityReflection|subject, chapter, month, strand, outcome, materials|
|TeacherObservation (+ type, parameters,<br>score, status) / ClassroomRecording|type (notebook, diary, syllabus, learning walk,<br>clinical…), observer, published / read / responded|
|BloomsTest / BloomsQuestion / BloomsMark;<br>DiagnosticAssessment / DiagnosticMark /<br>ScoreCard|chapter-end / topic / term-end|



### **addons — locked modules** 

Visitor, Visit, GatePass; InfirmaryVisit, Medicine; Alumni, AlumniEvent; Election, Nomination, Vote; Placement drive, Company, Offer; Franchise, Centre; PDC; ServiceSubscription; SQAADomain, Evidence; NAACCriterion, Evidence; AuditTemplate, AuditVisit; DocumentFolder, Document (versioned). Payroll, Recruitment and PMS sit in hr; Admissions Plus CRM and WhatsApp Marketing extend <mark>admissions</mark> and <mark>comms</mark> . 

### **Cross-cutting technical stack (recommended)** 

1. Multi-tenancy: organisation FK + middleware setting <mark>request.org</mark> , <mark>request.branch</mark> , <mark>request.ay</mark> from the header chips; custom managers filter by them. 

2. Permissions: Role → MenuItem → action flags, checked by a view mixin and used to render the mega-menu; access level (Org / Zonal / Branch / Staff / Class teacher) limits branch / section querysets. 

3. UI: Django templates + Bootstrap 5 + Lexend + Select2 + HTMX ( <mark>hx-get</mark> into <mark>#main</mark> , like MCB's <mark>#dvmain</mark> ), DataTables or a server-side table component with column picker and exports (openpyxl, CSV, WeasyPrint for PDF). 

4. Approvals: generic <mark>ApprovalFlow</mark> (type, levels, approver rule) + <mark>ApprovalRequest</mark> (generic FK, level, status, remarks, history). 

5. Background jobs: Celery + Redis for messaging, bulk uploads, report generation, payroll runs, VTS polling, automated alerts; Celery beat for schedules. 

6. Imports: one <mark>ImportJob</mark> model + per-type validators (enquiry, application, students, fee receivables, concessions, timetable, biometric, measurements, petty cash) with error-file download. 

7. Documents: HTML templates with <mark>@merge</mark> placeholders → WeasyPrint / LibreOffice for certificates, TC, ID cards, receipts, report cards, hall tickets, payslips. 

8. Integrations: payment gateways (Razorpay / PayU / CCAvenue webhooks), SMS DLT gateway, WhatsApp BSP, SMTP, FCM push, biometric / RFID push API, VTS vendor APIs, Tally export, Google / Microsoft OAuth, Zoom / Meet. 

9. APIs: Django REST Framework + JWT for parent, teacher, admin and pre-admission mobile apps. 10. Audit: django-simple-history (or a custom AuditLog) on Student, Staff, fee and receipt models; log report downloads with filters. 

## **Verification checklist** 

All 855 menu pages in the 47 active modules were fetched and checked against the live menu tree; none is missing. Where a page appears under two menus, it is written up once and noted. 

|Module|Menu pages|Documented|Notes|
|---|---|---|---|
|Organisation|24|24|—|
|SIS|46|46|—|
|Inventory|32|32|—|
|Dynamic forms|16|16|+ field deep-dive; no custom forms<br>exist|
|Learner Profile|12|12|—|
|Transport|35|35|—|
|Login Statistics|13|13|—|
|Certificates|23|23|TC Design returns MCB error page|
|Library|24|24|—|
|Hostel|35|35|Reports › Warden Details returns<br>MCB error page|
|Concerns|19|19|—|
|Achievements + Mentors|5|5|—|
|Finance|114|114|3 duplicates merged (Fee<br>Transaction Summary, Total Paid &<br>Due, Admission/strength reports)|
|School Store|38|38|Retried after a network drop|
|Expenses Management|17|17|—|
|Finance Intelligence|6|6|—|
|Admissions|56|56|2 duplicates (Pre-Admission details,|



|Module|Menu pages|Documented|Notes|
|---|---|---|---|
||||Walk-in survey)|
|HR|58|58|Inactive Staff Approvals listed under<br>2 menus|
|Staff Wall|4|4|—|
|SMS|6|6|—|
|WhatsApp|30|30|Haptik pages and "Others" senders<br>grouped|
|Email|17|17|—|
|Voice Calls|9|9|Voice subscription not active|
|Diary / Announcements /<br>Calendar / Gallery /<br>Notifications / Student Wall|33|33|—|
|CBSE and State|42|42|—|
|ECA and PET|10|10|—|
|IB / Cambridge / ICSE|39|39|Shared table (identical pages,<br>different suffix)|
|Pre School|13|13|—|
|Higher Ed|16|16|—|
|Exam Cell|14|14|—|
|LMS (9 modules)|49|49|Board-wise subject pages and MCB<br>resources grouped|
|**Total**|**855**|**855**||



Also covered: the Home dashboard (9 tabs and widgets), header utilities, module switcher (71 modules), and design tokens. 

Locked add-ons: this login can't open them, so the 24 modules are specified from MyClassboard's public knowledge base and product pages (see Locked add-ons). Result grids that appear only after pressing Get with real data selected aren't covered either, so their columns are listed only where the page returned them. A few Home dashboard tabs (Enrollment Review, Students M-o-M, Room Allocations, Classes in progress, Principal Diary) load their data by AJAX and were described from their tab titles. 

## **Sources (locked add-ons)** 

• <u>MCB Knowledge Base — Visitor Management</u> 

- <u>MCB KB — Payroll and page 2</u> 

- <u>MCB KB — HR Plus, HR Plus reports, Staf Recruitmentf</u> , Staf Assessmentf 

- <u>MCB KB — Mobile Apps</u> 

- MCB product pages: module index, HR Payroll, <u>Visitor Management, Infrmaryi</u> , Alumni, Student <u>Council, SQAA, Franchise, PDC, Automated Alerts, Admissions Plus CRM</u> 

