import os
import fitz  # PyMuPDF

SAMPLE_DOCS = {
    "Academic_Regulations.pdf": [
        ("Page 1: Academic Policies & Credit System",
         "ACADEMIC REGULATIONS & POLICIES\n\n"
         "1. Attendance Requirement: Students must maintain a minimum of 75% attendance in every course to be eligible to appear for the end-semester examinations. Shortage of attendance up to 10% may be condoned by the Principal on genuine medical grounds upon submission of valid medical certificates.\n\n"
         "2. Grading System: The college follows a 10-point Grading Scale (O, A+, A, B+, B, C, P, F). A minimum CGPA of 5.0 is required for graduation.\n\n"
         "3. Academic Integrity: Plagiarism, copying in examinations, or misrepresentation will lead to disciplinary action, including suspension or expulsion from the college."),
        ("Page 23: Examination Eligibility",
         "CHAPTER 4: SEMESTER EXAMINATION RULES\n\n"
         "Section 23: Minimum Attendance for Semester Exams.\n"
         "Students with attendance between 65% and 74% due to medical emergencies must submit medical documents within 3 days of resuming classes. Attendance below 65% under any circumstances will lead to detainment in the semester.\n\n"
         "Re-examination policy: Supplementary exams are conducted within 30 days of result publication for students failing up to 2 subjects.")
    ],
    "Fee_Structure.pdf": [
        ("Page 1: Tuition & Institutional Fees",
         "COLLEGE FEE STRUCTURE 2025-2026\n\n"
         "1. B.Tech Tuition Fee: INR 1,20,000 per annum (payable in two equal installments at the beginning of each semester).\n\n"
         "2. Development Fee: INR 15,000 per annum.\n\n"
         "3. Examination Fee: INR 2,500 per semester.\n\n"
         "4. Library Deposit (Refundable): INR 5,000 paid during admission.\n\n"
         "Payment Deadlines: Autumn semester fee due by August 15th; Spring semester fee due by January 15th. Late fee of INR 100 per day applies after the deadline.")
    ],
    "Hostel_Rules.pdf": [
        ("Page 1: Campus Residence Regulations",
         "HOSTEL RULES AND CODE OF CONDUCT\n\n"
         "1. Hostel Timings & In-Out Entry: All hostel residents must return to the campus hostel by 9:30 PM on weekdays and 10:00 PM on weekends. Entry after night curfew requires prior written permission from the Chief Warden.\n\n"
         "2. Visitor Rules: Female visitors are restricted to designated visitor lounges between 4:00 PM and 7:00 PM. No overnight guests are allowed without warden authorization.\n\n"
         "3. Quiet Hours: Strict silence must be observed from 11:00 PM to 6:00 AM in dormitory corridors and room blocks.")
    ],
    "Examination_Guidelines.pdf": [
        ("Page 7: Mid-Term and Final Exam Conduct",
         "EXAMINATION CENTRE GUIDELINES\n\n"
         "1. Hall Ticket Requirement: Students must carry their valid College ID card and Hall Ticket to the examination hall. Entry without ID is strictly prohibited.\n\n"
         "2. Electronic Devices: Mobile phones, smartwatches, programmable calculators, and Bluetooth gadgets are prohibited inside the examination hall.\n\n"
         "3. Exam Timings: Morning sessions run from 9:30 AM to 12:30 PM. Evening sessions run from 2:00 PM to 5:00 PM. No candidate will be admitted 30 minutes after commencement.")
    ],
    "Library_Rules.pdf": [
        ("Page 1: Central Library Operations",
         "CENTRAL LIBRARY TIMINGS & RESOURCES\n\n"
         "1. Library Hours: Open Monday to Saturday from 8:00 AM to 10:00 PM. During semester examinations, reading rooms remain open 24/7.\n\n"
         "2. Book Borrowing Limit: Undergraduate students may borrow up to 4 books for a duration of 14 days. Postgraduates may borrow up to 6 books for 30 days.\n\n"
         "3. Overdue Fines: Overdue books incur a fine of INR 5 per day per book.")
    ],
    "Placement_Information.pdf": [
        ("Page 1: Career Development & Placement Cell",
         "TRAINING AND PLACEMENT CELL GUIDELINES\n\n"
         "1. Eligibility: Students with CGPA 6.5 and above with no active backlogs are eligible for campus recruitment drives.\n\n"
         "2. One Student One Job Policy: Once a student receives a job offer of INR 6 LPA or above, they are considered placed and deregistered from further lower CTC recruitment drives.\n\n"
         "3. Internship Support: Summer internships are arranged for 3rd-year students across top tech companies and manufacturing firms during June-July.")
    ],
    "Scholarship_Information.pdf": [
        ("Page 1: Financial Aid and Merit Scholarships",
         "SCHOLARSHIP & FINANCIAL ASSISTANCE SCHEMES\n\n"
         "1. Merit-cum-Means Scholarship: Granted to students with annual family income below INR 3.0 Lakhs and CGPA above 8.0. Covers 50% of tuition fees.\n\n"
         "2. Institutional Academic Merit Award: Top 3 rank holders in each branch receive a waiver of INR 25,000 for the subsequent academic year.\n\n"
         "3. Application Period: Scholarship applications open in September every year via the Student Welfare Office portal.")
    ],
    "Electrical_Engineering_Specs.pdf": [
        ("Page 1: Electrical Engineering Department Standards",
         "DEPARTMENT OF ELECTRICAL ENGINEERING\n\n"
         "1. Lab Safety Requirements: All students attending High Voltage Lab and Power Electronics Lab must wear insulated non-conductive shoes and safety goggles.\n\n"
         "2. Lab Equipment Usage: Oscilloscopes, function generators, and power analyzers must be inspected before and after experiment sessions. Any equipment damage must be reported to the lab technician immediately.")
    ],
    "Computer_Science_Specs.pdf": [
        ("Page 1: Department of Computer Science & Engineering",
         "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n\n"
         "1. Computing Lab Facilities: The department operates 6 specialized labs (AI/ML Lab, Cloud Computing Lab, Cybersecurity Lab, Software Engineering Lab). Labs are accessible from 8:00 AM to 9:00 PM daily.\n\n"
         "2. Senior Capstone Project: Final year CSE students must complete a team capstone project incorporating RAG, Machine Learning, or Distributed Systems, mentored by faculty.")
    ]
}

def generate_pdfs(output_dir=None):
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_documents"))
    os.makedirs(output_dir, exist_ok=True)
    created_files = []

    for filename, pages in SAMPLE_DOCS.items():
        filepath = os.path.join(output_dir, filename)
        doc = fitz.open()

        for page_title, page_content in pages:
            page = doc.new_page(width=595, height=842)  # A4 size
            rect = fitz.Rect(50, 50, 545, 792)

            # Insert header and text
            text_to_write = f"--- {page_title} ---\n\n{page_content}"
            page.insert_textbox(rect, text_to_write, fontsize=11, fontname="helv")

        doc.save(filepath)
        doc.close()
        created_files.append(filepath)
        print(f"Generated sample PDF: {filepath}")

    return created_files

if __name__ == "__main__":
    generate_pdfs()
