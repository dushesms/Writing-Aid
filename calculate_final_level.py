import lexical_complexity_level_count as lex_cx
import models_grade_prediction as mod_pred
import pandas as pd
import altair as alt

def _calculate_grade(text):
    grade_1 = lex_cx.lex_dens_level(text)
    grade_2 = lex_cx.topic_level(text)
    grade_3 = mod_pred.predict_level(text)
    grade_final = round((grade_1+grade_2+grade_3)/3)
    return grade_final

def _build_graph(text):
    grade_final = _calculate_grade(text)
    df = pd.DataFrame.from_records( [
        {"CEFR level": "Basic user", "level": "A1", "number level": 1,
         "level description": "Can write simple isolated phrases and sentences on familiar topics of daily life situations (family, hobbies and pasttimes, holidays, leisure activities, shopping, and work and jobs)."},
        {"CEFR level": "Basic user", "level": "A2", "number level": 2,
         "level description": 'Can write a series of simple sentences on a familiar subject (education, hobbies and leisure activities, shopping, work and jobs, holidays) linked with simple connectors like "and", "but", and "because".'},
        {"CEFR level": "Independent user", "level": "B1", "number level": 3,
         "level description": "Can write straightforward connected texts on a range of familiar subjects (books, film, education, media, news, lifestyles and current affairs) within the field of interest, by linking a shorter discrete elements into a linear sequence."},
        {"CEFR level": "Independent user", "level": "B2", "number level": 4,
         "level description": "Can write clear, detailed texts on variety of subjects related to the field of interest (arts, books, film, media, news, and current affairs) synthesizing and evaluating information and arguments from a number of sources."},
        {"CEFR level": "Proficient user", "level": "C1", "number level": 5,
         "level description": "Can write clear, well-structured texts of complex subjects (scientific developments, technical and legal language, media, news, arts), underlining the relevant salient issues, expanding and supporting points of view at some length with subsidiary points, reasons and relevalnt examples, and rounding off with an appropriate conclusion."},
        {"CEFR level": "Proficient user", "level": "C2", "number level": 6,
         "level description": "Can write clear, smoothly flowing texts in an appropriate and effective style and a logical structure which helps the reader to find significant points."},
    ] )

    graph = alt.Chart(df).mark_bar().encode(
        x='level',
        y='number level',
        column='CEFR level',
        color=alt.condition(
            alt.FieldEqualPredicate(field='number level', equal = grade_final),
            alt.value('red'),
            alt.value('silver')
        ),
        tooltip=['level description'],
    ).interactive()

    return graph