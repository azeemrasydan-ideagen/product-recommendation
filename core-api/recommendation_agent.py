import requests
import json
from config import genai_api_url, genai_api_key
from db import db

def generate_payload(jobTitle, productUsed, searchQueries):
    instantPrompt = f"based on the products and product descriptions, as a user with jobTitle: {jobTitle}, productUsed: {productUsed}, and searchQueries: {', '.join(searchQueries)}, recommend 3 products, rank them based on the highest relevancy with percentage. Provide the answer in json array format. For the recommended products ensure that it is different from the product owned"
    
    text = """Ideagen Quality Management - QMS: Secure world class processes with our flagship QMS solution. Unlock data-driven decision making and secure world class processes that satisfy your customers and regulators, grow your business and achieve new quality standards with our flagship QMS solution.\nIdeagen EHS: The most integrated incident reporting and safety management solution. Powered by ProcessMAP, Ideagen EHS offers the most integrated incident reporting and safety management solution in the industry, giving safety managers a “single source of truth.\nIdeagen PleaseReview: Document review, co-authoring and redaction application that helps you to control and manage all aspects of the document creation and review process at scale.\nIdeagen Huddle: Create secure workspaces and portals to collaborate around content. Easier than email and file sharing, use Huddle to create secure workspaces and portals to collaborate around content, track activity, and communicate securely on projects or client engagements.\nIdeagen WorkRite RC: Our e-learning LMS designed to meet legal regulations. Transform your workplace compliance, with our e-learning and regulatory content. Designed to help you meet legal regulations and keep your staff healthy, happy and protected.\nIdeagen Quality Control: Balloon your part drawings and create your inspection sheets faster while ensuring 100% accuracy.\nIdeagen Supplier Management: Track and trace for a transparent supply chain. A Supply chain assurance solution that allows manufacturers to track raw materials and product movement through the supply chain, manage suppliers and supplier specifications and new product introductions.\nIdeagen Smartforms: Build secure mobile forms and applications. Simplify high-volume data collection and management through a low-code mobile smart forms solution that helps businesses and individuals save time, increase productivity, and make data-driven decisions. Integrate with your enterprise systems to handle all your mobile data collection.\nIdeagen Internal Audit: Delivers a complete, integrated audit lifecycle. Built by auditors for auditors, Pentana Audit delivers a complete, integrated audit lifecycle. It gives your internal audit team everything they need to provide assurance with confidence.\nIdeagen Risk Management: Ideagen Risk is the next generation of enterprise risk management software. It delivers seamless integration of assurance, risk, and compliance, with the best user experience.\nIdeagen Mail Manager: Control sensitive information and project correspondence for emails. Eliminate your email headache and control sensitive information and project correspondence.\nIdeagen Disclose: An automated disclosure checklist content tool. Disclose is an automated disclosure checklist content tool that makes it faster and easier to prepare financial statements and disclosures with accuracy.\nIdeagen Audit Analytics: Obtain quality audit data. Audit Analytics provides corporate gatekeepers and stakeholders with unique data and insights. Audit Analytics is used every day to empower accounting, financial, and academic professionals with the informative content critical to impact their work.\nIdeagen Quality Management - Qualtrax: Complete bundle of compliance management solutions. Qualtrax combines fully customizable process management with top-tier document management and control to boost the quality of your organization, especially in laboratories and the US federal and government sector."""

    retriever = db.as_retriever(
    search_type="mmr",  # Maximal Marginal Relevance for balancing relevance and diversity
    search_kwargs={
        "k": 5,  # Increase k to retrieve more candidates for ranking
        "lambda_mult": 0.8,  # Control relevance vs. diversity (closer to 1 is more relevance-focused)
    },
    )


    # Define the user's question
    query = f"a user with jobTitle: {jobTitle}, productUsed: {productUsed}, and searchQueries: {', '.join(searchQueries)}, recommend 3 products"

    # Retrieve relevant documents based on the query
    relevant_docs = retriever.invoke(query)
    context = f"{text}\n".join(doc.page_content for doc in relevant_docs)
    payload = {
        'data': json.dumps({
            "instantPrompt": instantPrompt,
            "text": context,
            "platform": 5
        })
    }
    return payload

def get_product_urls():
    return {
        "Ideagen Quality Management - QMS": "https://go.ideagen.com/ideagen-home-q-pulse-qms",
        "Ideagen EHS": "https://go.ideagen.com/ideagen-home-ideagen-ehs",
        "Ideagen PleaseReview": "https://go.ideagen.com/ideagen-home-pleasereview",
        "Ideagen Huddle": "https://go.ideagen.com/ideagen-home-huddle",
        "Ideagen WorkRite RC": "https://go.ideagen.com/ideagen-home-workrite",
        "Ideagen Quality Control": "https://go.ideagen.com/ideagen-home-q-pulse-pm",
        "Ideagen Supplier Management": "https://go.ideagen.com/ideagen-home-qadex",
        "Ideagen Smartforms": "https://go.ideagen.com/ideagen-home-mi-co",
        "Ideagen Internal Audit": "https://go.ideagen.com/ideagen-home-pentana-audit",
        "Ideagen Risk Management": "https://go.ideagen.com/ideagen-home-pentana-risk",
        "Ideagen Mail Manager": "https://go.ideagen.com/ideagen-home-mail-manager",
        "Ideagen Disclose": "https://go.ideagen.com/ideagen-home-pentana-disclose",
        "Ideagen Audit Analytics": "https://go.ideagen.com/ideagen-home-audit-analytics",
        "Ideagen Quality Management - Qualtrax": "https://go.ideagen.com/ideagen-home-q-pulse-qms"
    }

def recommend(payload):
    url = "https://idea-gen-ai-igh.ideagendevai.com/api/idea-gen-ai-service/v2/prompts/15a57fc3-cd0c-4aac-87af-6db3ac1ee0ad"

    headers = {
        'x-api-key': 'api key',
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

    # Get product URLs
    product_urls = get_product_urls()

    # Create a dictionary to store the products, their descriptions, and URLs
    products = {item["product"]: {"description": item["description"], "url": product_urls.get(item["product"], "#")} for item in products_data}
    return products