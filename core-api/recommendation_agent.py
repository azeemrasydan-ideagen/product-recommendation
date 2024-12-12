import requests
import json

def generate_payload(jobTitle, productUsed, searchQueries):
    instantPrompt = f"based on the products and product descriptions, as a user with jobTitle: {jobTitle}, productUsed: {productUsed}, and searchQueries: {', '.join(searchQueries)}, recommend 3 products, rank them based on the highest relevancy with percentage. Provide the answer in json array format. For the recommended products ensure that it is different from the product owned"
    
    text = """Audit Analytics: Provides unique data and insights to empower accounting, financial, and academic professionals with informative content critical for their work.\nCompliancePath: Validates your QMS to 21 CFR Part 11 and harmonizes your policy and privacy frameworks to HIPAA, HITRUST, IEC62304, 21 CFR Part 820, and any area of Health IT or Life Science convergence.\nCompliSpace: Built on the four pillars of policy, learning, assurance, and reporting, helping you achieve 'policy to culture.'\nCoruson: Enables transport companies to gain complete control, visibility, and real-time reporting of their safety and operational risks.\nDevonWay: Provides a fully integrated, configurable product suite across environmental, health and safety, quality management, enterprise asset management, and workforce management.\nHuddle: Offers secure file sharing and document collaboration for internal and external teams, enabling content collaboration, activity tracking, and project communication in a shared environment.\nIdeagen Academy: Offers interactive demos, online learning, and assessments to help your workforce become proficient with Ideagen software.\nIdeagen EHS: Powered by ProcessMAP, provides an integrated incident reporting and safety management solution, giving safety managers a 'single source of truth.'\nIdeagen Mail Manager: Eliminates email headaches and ensures control of sensitive information and project correspondence.\nInspectionXpert: Facilitates faster and accurate creation of ballooned part drawings and inspection sheets. Now integrated as Ideagen Quality Control.\nMedforce: Offers process and document management solutions tailored for US healthcare. Acquired by Ideagen in 2018.\nOpsbase: A user-friendly, paperless checklist and inspection platform acquired by Ideagen in 2021.\nOp Central: An AI-powered global software platform specializing in managing SOPs, training, audits, communications, and incidents for franchises and multi-site organizations.\nOnePlace Solutions: Integrates Office 365 tools like Outlook, SharePoint, Teams, and OneDrive for intelligent information management, compliance, and collaboration.\nPentana Audit: Provides an integrated audit lifecycle tool, supporting internal audit teams with confidence. Now known as Ideagen Internal Audit.\nPentana Disclose: An automated accounts disclosure checklist tool for efficient tailoring, reviewing, and approval. Now called Ideagen Disclose.\nPentana Risk: Offers complete visibility and control over organizational risks, helping build resilience and compliance. Now Ideagen Risk Management.\nPlant Assessor: The world's largest platform for plant and equipment safety and information sharing, tailored for machinery users.\nPleaseReview: A secure collaborative platform for document review, co-authoring, and redaction, enabling efficient control of document workflows.\nProquis: A quality management solution now replaced by Ideagen Quality Management.\nProcessMAP: Acquired by Ideagen in 2022, a leading solution for digitalizing and transforming environmental, health, and safety management initiatives. Now Ideagen EHS.\nQADEX: [No description provided.]\nQualsys: Acquired by Ideagen in 2020, it provides a primary quality management solution now known as Ideagen Quality Management.\nQualtrax: Combines customizable process and document management, especially for laboratories and government sectors in the US.\nQ-Pulse EHS: Formerly the Scannell EHS management solution, it is now Ideagen EHS, a workplace safety solution.\nQ-Pulse Law: A regulatory content service acquired by Ideagen in 2019, formerly Scannell Solutions, now called Q-Pulse Law.\nQ-Pulse OSHENS: [No description provided.]\nQ-Pulse PM: Automates First Article Inspection (FAI), Production Part Approval Process (PPAP), and New Product Introduction (NPI) for quality documentation and customer relationships.\nQ-Pulse QMS: Acquired by Ideagen in 2015, a leading name in quality management digitalization. Now Ideagen Quality Management.\nQ-Pulse Risk: A tool leveraging standardized risk models to manage risks effectively, aiding decision-making through impact analysis and risk modeling.\nQ-Pulse SP: Enables suppliers to submit quality documentation via a web portal, with approval tools for submissions and part shipments.\nQ-Pulse WorkRite: Transforms workplace training with an e-Learning LMS designed to meet legal regulations and protect staff. Now Ideagen WorkRite.\nRisk Management: A next-generation enterprise risk management solution delivering integration of assurance, risk, and compliance with excellent user experience.\nSmartforms: Simplifies high-volume data collection with a low-code mobile solution that saves time and enhances productivity, integrating with enterprise systems.\nTritan Software: Helps maritime operators maintain health and safety best practices across global fleets, improving compliance, uptime, and operations.\nWorkbench: A quality management solution now replaced by Ideagen Quality Management.\nIdeagen WorkRite: An e-Learning LMS designed to meet legal regulations and ensure staff well-being."""

    payload = {
        'data': json.dumps({
            "instantPrompt": instantPrompt,
            "text": text,
            "platform": 5
        })
    }
    return payload

def recommend(payload):
    url = "api-key"

    headers = {
        'x-api-key': 'api_key',
        'productInstanceId': '987e6543-e21b-23d4-a789-426614173999',
        'tenantId': 'f97df110-f4de-492e-8849-4a6af68026b0'
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)
    # Parse the JSON response
    response_data = json.loads(response.text)

    # Extract the answer text containing product names and descriptions
    answer_text = response_data["data"]["answer"]["answerText"]

    # Remove the surrounding markdown code block
    answer_text = answer_text.strip("```json\n").strip("\n```")

    # Parse the JSON content inside the answer text
    products_data = json.loads(answer_text)

    # Create a dictionary to store the products and their descriptions
    products = {item["product"]: item["description"] for item in products_data}
    return products