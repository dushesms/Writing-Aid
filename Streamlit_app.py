import base64
import time
import streamlit as st
from PIL import Image
import grammar_spell as spell_with_grammar_checker
import lexical_complexity_level_count as lcx
import topic_recognition
import predict_grade
import calculate_final_level

@st.cache( allow_output_mutation=True )
def get_base64_of_bin_file(bin_file):
    with open( bin_file, 'rb' ) as f:
        data = f.read()
    return base64.b64encode( data ).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    '''% bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('language app.png')

st.title('Typewriter :heart::flag-gb:')


img = Image.open("typewriter.png")
st.image(img)
st.subheader('This tool can help assess your English based on your writing. It will also give recommendations on how to improve it.')
color = st.select_slider('Rate yourself as an English writer',
                         options=['Terrible', 'Quite bad', 'Decent', 'Pretty Good', 'Excellent'])

st.write("Now you can check what the 'Typewriter' says. Write your text or paste from a document and see the results.")

option = st.selectbox('Choose what you want to check: ',
    ['Check your writing', 'Understand the results'])

if option == 'Check your writing':
    my_slot = st.empty()
    st.write( "Please, fill in the text field with your great writing." )
    text = st.text_area( label='writing', value="Type here..." )
    answer = my_slot.radio(
        'Which aspect of your writing do you want to check?',
        ['1. Spelling and Grammar',
         '2. Lexis and topics complexity',
         '3. Predicted grade'] )

    if answer == '1. Spelling and Grammar':
        st.write("You can see if you have any mistakes and their percent % in the whole text. Lower number means fewer mistakes.")
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        with st.spinner('Please wait while we are checking your work'):
            time.sleep(10)
        st.success('Done!')
        spell_with_grammar_checker.example_check(text)
    elif answer == '2. Lexis and topics complexity':
        st.write("The more advanced vocabulary you use, the higher is your level of English.")
        st.write( 'There are 6 levels of English where 1 means "Beginner" and 6 is "Proficient".' )
        st.write( "Lexical density shows the percentage of words of each level in the whole text." )
        st.write("The words were taken from the Language Portfolio which is the minimum of words chosen for each level. There are 1500-2500 words for a level approximately.")
        st.write('Predicted topic: {topic}.'.format(topic= topic_recognition.predict_topic(text)))
        lcx.topic_level(text)
        lcx.write_lex_density(text)
    elif answer == '3. Predicted grade':
        st.write("Your predicted grade is {num}% which corresponds to grade {letter}.".format(num=predict_grade.text_predict(text), letter= predict_grade.grade_converter(predict_grade.text_predict(text))))
elif option == 'Understand the results':
    text = st.text_area(label='writing', value="Type here..." )
    st.write("There are six levels of English according to CEFR.")
    st.write( "Your calculated level is marked RED." )
    chart = calculate_final_level._build_graph(text)
    st.altair_chart(chart)
    st.write("See what your level is and read descriptions of each level.")
