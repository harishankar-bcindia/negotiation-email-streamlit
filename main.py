import streamlit as st


from gpt_call import analyze_email_reply_by_gpt
from send_email_template import send_template


st.set_page_config(
    page_title="Negotiation app",
    layout="wide",  # Set layout to wide mode
    initial_sidebar_state="auto"
)

# # Initialize session state variables
# if 'counter' not in st.session_state:
#     st.session_state.counter = 0


# # Function to increment the counter
# def increment_counter():
#     st.session_state.counter += 1

# Initialize session state variables if they do not exist
if 'supplier_name' not in st.session_state:
    st.session_state.supplier_name = None
if 'po_description' not in st.session_state:
    st.session_state.po_description = None
if 'po_amount' not in st.session_state:
    st.session_state.po_amount = None
if 'email_body' not in st.session_state:
    st.session_state.email_body = None
if 'negotiation_tone' not in st.session_state:
    st.session_state.negotiation_tone = None
if 'editable_template' not in st.session_state:
    st.session_state.editable_template = None

if 'output1' not in st.session_state:
    st.session_state.output1 = False


if 'gpt_output' not in st.session_state:
    st.session_state.gpt_output = False

if 'template' not in st.session_state:
    st.session_state.template = False

# Main function to run the Streamlit app
def main():
    # Title of the app
    st.title("Negotiation email template generator")

    # Text inputs
    supplier_name = st.text_input("Supplier name")
    st.session_state.supplier_name = supplier_name

    po_description = st.text_input("PO description")
    st.session_state.po_description = po_description

    po_amount = st.text_input("PO amount")
    st.session_state.po_amount = po_amount

    email_body = st.text_area("Email body")
    st.session_state.email_body = email_body

    tone = st.slider("Negotiation tone",1,10)
    st.session_state.tone = tone


    # Check if all inputs are filled
    if supplier_name and po_description and po_amount and email_body:
        # Enable button if all inputs are filled
        if st.button("Generate template"):
            with st.spinner("Generating template..."):
                output = analyze_email_reply_by_gpt(
                    email_body,
                    po_description,
                    supplier_name,
                    po_amount,
                    tone)
                st.session_state.output1 = output

                st.session_state.gpt_output = True

        if st.session_state.gpt_output:
            st.session_state.editable_template = st.text_area("Edit template:", st.session_state.output1)
            user_first_name = st.text_input("Enter user first name:")
            message_id = st.text_input("Enter Message ID:")
            supplier_name = st.session_state.supplier_name
            po_description = st.session_state.po_description
            if user_first_name and message_id:
                if st.button("Send template"):
                    output2 = send_template(user_first_name,supplier_name,po_description,st.session_state.editable_template,message_id)
                    st.write(output2)

                # Optionally, you can use the edited text for further processing
    else:
        # Inform user to fill all inputs
        st.write("Please fill all the inputs to generate email template.")

# Run the main function
if __name__ == "__main__":
    main()


# supplier = "Amazon"
# description = "Laptops and Tablets purchase for new joiners"
# amount = "100000 GBP"
# tone = 9
# email_body = '''
# Hi Kloo,
#                 I need to request a negotiation on the amount of the purchase order for the supplier {supplier}.
#                 Tactic to negotiate with supplier is: Cite lower cost alternatives

#                 Regards,
#                 Harishankr Vashishtha
#                 Associate Data Science

#             '''
# print(analyze_email_reply_by_gpt(email_body,description,supplier,amount,tone))
