import streamlit as st

from bagels.bagels import Bagels


bagels = Bagels()
st.title(bagels.title)
with st.sidebar:
    st.text(bagels.intro)
    if st.button("Start Game"):
        bagels.set_secret_num()


st.text(bagels.new_game_message)


guess_count = bagels.get_guess_count()
guess = st.text_input("Guess #{}".format(guess_count))
if st.button("Submit Guess"):
    if str(guess) == str(bagels.secret_num):
        st.success("You got it!")
        st.balloons()
    else:
        clues = bagels.get_clues(guess)
        st.info(clues)

        if int(guess_count) >= 10:
            bagels.reset_guess_count()

        else:
            bagels.update_guess_count(guess_count)

