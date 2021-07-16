import os
import streamlit.components.v1 as components
import streamlit as st
from htbuilder import HtmlElement, div, span, styles, classes, fonts
from htbuilder.units import percent, px, rem, em


def annotation(body, label="", background="#ddd", color="#333", **style):

    if "font_family" not in style:
        style["font_family"] = "sans-serif"

    return span(
        style=styles(
            background=background,
            border_radius=rem(0.43),
            color=color,
            padding=(rem(0.05), rem(0.02)),
            display="inline-flex",
            justify_content="center",
            align_items="center",
            **style,
        )
    )(
        body,
        span(
            style=styles(
                color=color,
                font_size=em(0.67),
                opacity=0.5,
                text_transform="uppercase"
            )
        )(label)
    )

def annotated_text(l, *args, **kwargs):

    out = div(style=styles(
        font_family="sans-serif",
        line_height="1.3",
        font_size=px(16),
    ))

    for arg in args:
        if isinstance(arg, str):
            h = len(arg)/16*35
            out(arg)

        elif isinstance(arg, HtmlElement):
            out(arg)

        elif isinstance(arg, tuple):
            out(annotation(*arg))

        else:
            raise Exception("Oh noes!")

    components.html(str(out), height=l, **kwargs)

_RELEASE = False

if not _RELEASE:
    _st_lottie = components.declare_component(
        "streamlit_lottie", url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_lottie = components.declare_component("streamlit_lottie", path=build_dir)

def st_lottie():
    pass