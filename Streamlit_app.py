import streamlit as st
from PIL import Image
import topic_recognition
import grammar_spell as spell_with_grammar_checker
import time
import lexical_complexity_level_count as lcx
import base64
import assessment_level

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
    ''' % bin_str

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
    ['Check your writing', 'See the results'])

if option == 'Check your writing':
    my_slot = st.empty()
    st.write( "Please, fill in the text field with your great writing." )
    text = st.text_area( label='writing', value="Type here..." )
    answer = my_slot.radio(
        'Which aspect of your writing do you want to check?',
        ['1. Spelling and Grammar',
         '2. Lexis and topics complexity',
         '3. Graded in comparison with similar works'] )

    if answer == '1. Spelling and Grammar':
        st.write("You can see if you have any mistakes and their percent % in the whole text. Lower number means fewer mistakes.")
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress( percent_complete + 1 )
        with st.spinner('Please wait while we check your work'):
            time.sleep(10)
        st.success('Done!')
        spell_with_grammar_checker.example_check(text)
    elif answer == '2. Lexis and topics complexity':
        st.write("The more advanced vocabulary you use, the higher is your level of English.")
        st.write('Predicted topic: ', topic_recognition.predict_topic(text))
        lcx._lang_level(text)
    elif answer == '3. Graded in comparison with similar works':
        st.write("This feature is still in progress. It seems like your predicted level is ", assessment_level.predict(text))
elif option == 'See the results':
    st.write("There are six levels of English according to CEFR: ")
    levels_img = Image.open("file.png")
    st.image(levels_img)
    st.write("See what your level is and read descriptions of each level. ")


