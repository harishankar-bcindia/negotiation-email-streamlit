import streamlit as st


from gpt_call import analyze_email_reply_by_gpt

st.set_page_config(
    page_title="Negotiation app",
    layout="wide",  # Set layout to wide mode
    initial_sidebar_state="auto"
)

# Main function to run the Streamlit app
def main():
    # Title of the app
    st.title("Negotiation email template generator")

    # Text inputs
    supplier = st.text_input("Supplier name")
    description = st.text_input("PO description")
    amount = st.text_input("PO amount")

    # Long text input
    email_body = st.text_area("Email body")

    # Slider input
    tone = st.slider("Negotiation tone", 1, 10)

    # Check if all inputs are filled
    if supplier and description and amount and email_body:
        # Enable button if all inputs are filled
        if st.button("Generate template"):
            with st.spinner("Generating template..."):
                output = analyze_email_reply_by_gpt(email_body,description,supplier,amount,tone)
                st.write(output)
    else:
        # Inform user to fill all inputs
        st.write("Please fill all the inputs to enable the button.")

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
