"""Slide bodies for carousels. Each function returns the HTML that goes inside a Deck slide (brand.Deck.add).
Text rules: headline 3 to 7 words, at most ~25 words of body per slide, digits on screen, no em dashes."""

from brand import bubbles


def cover(hook, chip):
    """Slide 1: the hook (6 words or fewer) and the empty bubble row. Kept inside the grid's 3:4 crop."""
    return (f'<div style="margin-top:200px"><span class=chip>{chip}</span>'
            f'<h1 style="margin-top:40px">{hook}</h1><div style="margin-top:70px">{bubbles()}</div></div>')


def stake(headline, body):
    """Slide 2: why it matters. Also works as a second cover if Instagram re-shows the carousel from slide 2."""
    return f'<div style="margin-top:210px"><h2>{headline}</h2><p style="margin-top:44px">{body}</p></div>'


def question(stem_paragraphs, choices):
    paras = "".join(f'<p style="margin-top:{0 if i == 0 else 30}px">{p}</p>' for i, p in enumerate(stem_paragraphs))
    opts = "<br>".join(f"({l}) {v}" for l, v in choices.items())
    return (f'<div style="margin-top:90px">{paras}<div class=choices style="margin-top:44px">{opts}</div>'
            f'<p style="margin-top:36px;font-size:32px;opacity:.75">Pick one before you swipe.</p></div>')


def solve(headline, lines, note=None):
    """One idea per slide: a headline and up to 4 lines of working."""
    math = "<br>".join(lines)
    extra = f'<p style="margin-top:44px">{note}</p>' if note else ""
    return (f'<div style="margin-top:120px"><h2>{headline}</h2>'
            f'<div class=math style="margin-top:56px">{math}</div>{extra}</div>')


def answer(headline, letter, note):
    return (f'<div style="margin-top:150px"><h2>{headline}</h2><div style="margin-top:60px">{bubbles(letter)}</div>'
            f'<p style="margin-top:56px">{note}</p></div>')


def trap(letter, headline, body):
    return (f'<div style="margin-top:150px"><span class=chip>Trap answer: {letter}</span>'
            f'<h2 style="margin-top:40px">{headline}</h2><p style="margin-top:44px">{body}</p></div>')


def recap(headline, rule, example):
    """The screenshot slide: readable with no context."""
    return (f'<div style="margin-top:150px"><span class=chip>Save this</span><h2 style="margin-top:40px">{headline}</h2>'
            f'<p style="margin-top:44px"><b>{rule}</b></p><div class=math style="margin-top:44px">{example}</div></div>')


def cta(headline, body):
    return (f'<div style="margin-top:260px"><h1 style="font-size:96px">{headline}</h1>'
            f'<p style="margin-top:50px">{body}</p></div>')
