from django.core.management.base import BaseCommand
from applicant.models import Job
import random

class Command(BaseCommand):
    help = 'Add unique test jobs to the database'

    def handle(self, *args, **kwargs):
        # Define some sample job titles, descriptions, and skills
        job_titles = [
            "Software Engineer", "Data Scientist", "Web Developer", "Product Manager",
            "UX Designer", "Quality Assurance Engineer", "Project Manager", "Business Analyst",
            "Data Engineer", "System Architect", "Mobile Developer", "DevOps Engineer",
            "Cloud Engineer", "Security Analyst", "Frontend Developer", "Backend Developer",
            "Machine Learning Engineer", "Game Developer", "Network Administrator", 
            "System Administrator", "Full Stack Developer", "Database Administrator", 
            "IT Support Specialist", "Content Strategist", "Digital Marketing Manager",
            "Customer Service Representative", "Virtual Assistant", "Sales Executive",
            "Human Resources Specialist", "Accountant", "Marketing Assistant", 
            "Call Center Agent", "Operations Manager", "Administrative Assistant",
            "Graphic Designer", "Web Content Writer", "Social Media Specialist", "Tech Support"
        ]
        
        job_descriptions = [
            "Develop and maintain software applications.",
            "Analyze data to help businesses make informed decisions.",
            "Design and build websites and web applications.",
            "Manage product development from concept to release.",
            "Design user-friendly and functional interfaces.",
            "Ensure the quality of software through testing.",
            "Lead project teams to deliver software solutions.",
            "Analyze business needs and develop software solutions.",
            "Design and implement data systems and pipelines.",
            "Architect complex systems and manage scalability.",
            "Design and develop mobile applications for iOS and Android.",
            "Automate infrastructure and manage CI/CD pipelines.",
            "Manage and optimize cloud infrastructure services.",
            "Protect systems and data from cyber threats.",
            "Design and build the user interface of web applications.",
            "Design and implement server-side applications.",
            "Create and deploy machine learning models and algorithms.",
            "Develop interactive video games across multiple platforms.",
            "Maintain network infrastructure and ensure connectivity.",
            "Install, configure, and manage systems and networks.",
            "Develop full-stack applications with a variety of frameworks.",
            "Administer databases and ensure data integrity and security.",
            "Provide technical support and assistance to end users.",
            "Develop content strategies and manage content creation.",
            "Create and execute digital marketing campaigns.",
            "Respond to customer inquiries and resolve issues efficiently.",
            "Assist clients with administrative tasks remotely.",
            "Sell products or services and meet sales targets.",
            "Perform HR tasks including recruitment and employee relations.",
            "Prepare financial reports and manage accounting tasks.",
            "Create social media content and help manage online presence.",
            "Provide customer support and handle technical issues.",
            "Create and design graphics for various platforms and media."
        ]
        
        job_skills = [
            "Python, Django, JavaScript", "Python, Data Analysis, Machine Learning", 
            "HTML, CSS, JavaScript, React", "Agile, Scrum, Product Development", 
            "UX/UI Design, Figma, Adobe XD", "Automation, Testing, CI/CD", 
            "Project Management, Jira, Scrum", "Business Analysis, SQL, Data Modeling", 
            "Python, SQL, ETL, Hadoop", "Java, AWS, Microservices", "Swift, Objective-C, iOS",
            "Docker, Kubernetes, AWS, Azure", "Linux, Bash, Git, Cloud Services", 
            "Penetration Testing, Cybersecurity, Network Security", "JavaScript, HTML, CSS, Vue.js",
            "Node.js, Express, MongoDB, REST APIs", "Machine Learning, TensorFlow, Deep Learning", 
            "C#, Unity, Unreal Engine", "Networking, VPNs, TCP/IP, Routers", "Linux, Cloud, AWS, GCP",
            "Java, SQL, Spring, Hibernate", "SQL, PostgreSQL, MySQL, MongoDB", "Windows Server, Active Directory",
            "Content Marketing, SEO, Social Media, Analytics", "Google Ads, SEO, Facebook Ads, Marketing Strategy",
            "Customer Support, CRM Software, Communication", "Time Management, Scheduling, MS Office",
            "Salesforce, Negotiation, CRM, B2B Sales", "Accounting Software, Financial Reporting, Budgeting",
            "Graphic Design, Adobe Photoshop, Illustrator", "Social Media Marketing, Copywriting, SEO",
            "Tech Support, Troubleshooting, Networking", "Virtual Assistance, Email Management, Calendar Management"
        ]

        # Generate 20,000 unique jobs
        created_jobs = set()
        for _ in range(20000):
            # Create a unique combination of title, description, and skills
            title = random.choice(job_titles)
            description = random.choice(job_descriptions)
            skills = random.choice(job_skills)

            # Ensure uniqueness by checking combinations
            job_entry = (title, description, skills)
            while job_entry in created_jobs:
                title = random.choice(job_titles)
                description = random.choice(job_descriptions)
                skills = random.choice(job_skills)
                job_entry = (title, description, skills)

            # Add the combination to the set to track uniqueness
            created_jobs.add(job_entry)
            
            # Create a new job entry in the database
            Job.objects.create(
                title=title,
                description=description,
                required_skills=skills
            )

        self.stdout.write(self.style.SUCCESS('Successfully added 20,000 unique test jobs!'))
