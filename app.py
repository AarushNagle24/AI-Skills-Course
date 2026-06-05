from html import escape
import random
from textwrap import dedent
from urllib.parse import quote

import streamlit as st

from auth import hash_password, verify_password
from course_templates import COURSE_CONTENT_TEMPLATES, SAMPLE_COURSES
from database import (
    change_user_password,
    create_contact_request,
    create_course_from_key,
    create_user,
    delete_admin_course,
    enroll_user_in_course,
    get_admin_course,
    get_admin_courses,
    get_course_for_learning,
    get_enrolled_courses,
    get_progress,
    get_user_by_id,
    get_user_by_username,
    init_db,
    leave_course,
    mark_course_step_completed,
    mark_reading_viewed,
    regenerate_join_code,
    remove_employee_from_course,
    update_course_details,
    validate_creation_key,
)
from ui_components import inject_css, page_title, public_nav


st.set_page_config(
    page_title="AI Skills Course Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()
inject_css()

TOTAL_COURSE_STEPS = 5


def init_session_state() -> None:
    defaults = {
        "logged_in": False,
        "user_id": None,
        "username": "",
        "current_platform_page": "login",
        "selected_course_id": None,
        "selected_admin_course_id": None,
        "course_view_step": 1,
        "selected_sample_course": None,
        "sample_course_progress": {},
        "pending_creation_key": "",
        "pending_leave_course_id": None,
        "account_menu_open": False,
        "account_created": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def get_query_page() -> str:
    page = st.query_params.get("page", "home")
    if isinstance(page, list):
        page = page[0] if page else "home"
    return page or "home"


def set_public_page(page: str) -> None:
    st.query_params["page"] = page


def get_query_value(name: str, default: str) -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value or default


def get_query_int(name: str, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(get_query_value(name, str(default)))
    except ValueError:
        value = default
    return max(minimum, min(maximum, value))


def go_platform(page: str) -> None:
    st.session_state.current_platform_page = page
    st.rerun()


def sample_course_url(template_idx: int, step: int = 1, view: str = "reading", completed: int = 0) -> str:
    return f"?page=sample_course&template={template_idx}&step={step}&view={view}&completed={completed}"


def sample_course_thumbnail(title: str, idx: int) -> str:
    palettes = [
        ("#f6f8fb", "#dbe3ef", "#8ea0b8", "#fefefe"),
        ("#f8f7f4", "#e8ded1", "#a19078", "#ffffff"),
        ("#f7f9f7", "#dce9df", "#7f9d89", "#ffffff"),
        ("#f8f7fb", "#e1ddec", "#9187aa", "#ffffff"),
    ]
    bg, panel, accent, white = palettes[idx % len(palettes)]
    label = escape(title.split(" for ")[-1].replace(" and ", " + "))
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" role="img" aria-label="{escape(title)} thumbnail">
        <rect width="960" height="520" rx="42" fill="{bg}"/>
        <rect x="88" y="78" width="784" height="364" rx="34" fill="{white}" stroke="{panel}" stroke-width="5"/>
        <rect x="132" y="124" width="310" height="34" rx="17" fill="{panel}"/>
        <rect x="132" y="188" width="492" height="26" rx="13" fill="{panel}"/>
        <rect x="132" y="240" width="420" height="26" rx="13" fill="{panel}"/>
        <rect x="132" y="292" width="520" height="26" rx="13" fill="{panel}"/>
        <circle cx="742" cy="225" r="74" fill="{accent}" opacity="0.92"/>
        <path d="M704 225h76M742 187v76" stroke="{white}" stroke-width="18" stroke-linecap="round"/>
        <rect x="626" y="334" width="190" height="44" rx="22" fill="{panel}"/>
        <text x="132" y="392" fill="{accent}" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="700">{label}</text>
    </svg>
    """
    return f"data:image/svg+xml;charset=utf-8,{quote(svg)}"


def course_thumbnail(title: str, idx: int) -> str:
    palettes = [
        ("#f6f8fb", "#dbe3ef", "#8ea0b8", "#fefefe"),
        ("#f8f7f4", "#e8ded1", "#a19078", "#ffffff"),
        ("#f7f9f7", "#dce9df", "#7f9d89", "#ffffff"),
        ("#f8f7fb", "#e1ddec", "#9187aa", "#ffffff"),
    ]
    bg, panel, accent, white = palettes[idx % len(palettes)]
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" role="img" aria-label="{escape(title)} thumbnail">
        <rect width="960" height="520" rx="42" fill="{bg}"/>
        <rect x="88" y="78" width="784" height="364" rx="34" fill="{white}" stroke="{panel}" stroke-width="5"/>
        <rect x="132" y="126" width="310" height="34" rx="17" fill="{panel}"/>
        <rect x="132" y="190" width="492" height="26" rx="13" fill="{panel}"/>
        <rect x="132" y="242" width="420" height="26" rx="13" fill="{panel}"/>
        <rect x="132" y="294" width="520" height="26" rx="13" fill="{panel}"/>
        <circle cx="742" cy="225" r="74" fill="{accent}" opacity="0.92"/>
        <path d="M704 225h76M742 187v76" stroke="{white}" stroke-width="18" stroke-linecap="round"/>
        <rect x="626" y="334" width="190" height="44" rx="22" fill="{panel}"/>
    </svg>
    """
    return f"data:image/svg+xml;charset=utf-8,{quote(svg)}"


def completed_steps_from_percent(progress_percent: int | None) -> int:
    return max(0, min(TOTAL_COURSE_STEPS, int(progress_percent or 0) // 20))


def progress_percent_from_steps(completed_steps: int) -> int:
    return max(0, min(TOTAL_COURSE_STEPS, completed_steps)) * 20


def current_step_from_progress(progress_percent: int | None) -> int:
    completed_steps = completed_steps_from_percent(progress_percent)
    return min(TOTAL_COURSE_STEPS, completed_steps + 1)


def render_step_progress(total_steps: int, completed_steps: int, current_step: int | None = None, compact: bool = False) -> None:
    classes = "sample-progress card-progress" if compact else "sample-progress"
    parts = [f'<div class="{classes}" aria-label="Course progress">']
    for step in range(1, total_steps + 1):
        state = "completed" if step <= completed_steps else "active" if step == current_step else "upcoming"
        parts.append(f'<div class="progress-circle {state}">{step}</div>')
        if step < total_steps:
            line_state = "completed" if step <= completed_steps else "upcoming"
            parts.append(f'<div class="progress-line {line_state}"></div>')
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def reading_markup(reading: str) -> str:
    paragraphs = [block.strip() for block in reading.strip().split("\n\n") if block.strip()]
    return "".join(f"<p>{escape(paragraph).replace(chr(10), '<br>')}</p>" for paragraph in paragraphs)


def get_module_questions(module: dict) -> list[dict]:
    if "questions" in module:
        return module["questions"]
    return [
        {
            "question": module["question"],
            "options": module["options"],
            "correct": module["correct"],
        }
    ]


def shuffled_answer_options(question: dict, state_key: str) -> list[str]:
    options = list(question["options"])
    saved_options = st.session_state.get(state_key)
    if saved_options and sorted(saved_options) == sorted(options):
        return saved_options

    shuffled = options[:]
    random.shuffle(shuffled)
    st.session_state[state_key] = shuffled
    return shuffled


def card(title: str, body: str, meta: str = "") -> None:
    meta_html = f'<div class="card-meta">{meta}</div>' if meta else ""
    st.markdown(
        f"""
        <div class="soft-card fade-in">
            <h3>{title}</h3>
            {meta_html}
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    public_nav("home")
    st.markdown(
        """
        <section class="hero fade-in">
            <div class="hero-kicker">Private AI training for working teams</div>
            <h1>AI courses built around your work</h1>
            <p>
                Tell us what your team does and where AI could help. We design a private course with lessons,
                quizzes, progress tracking, and admin tools for your company.
            </p>
            <div class="hero-actions">
                <a href="?page=sample_courses" target="_self" class="ghost-button">View sample courses</a>
                <a href="?page=contact" target="_self" class="light-button">Contact us</a>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section home-centered fade-in">', unsafe_allow_html=True)
    page_title(
        "Training employees can use at work",
        "Tell us about your roles, workflows, goals, and AI policies. We use those details to shape a course around real employee tasks, so your team learns practical AI habits they can use right away.",
        centered=True,
    )
    cols = st.columns(3)
    with cols[0]:
        card(
            "Tailored to your team",
            "We shape each course around your team’s roles, tools, workflows, and internal policies so the training feels relevant to their work",
            "Custom content",
        )
    with cols[1]:
        card(
            "Simple employee access",
            "Employees join with a private course code, complete lessons and quizzes, and track their progress from their own course dashboard",
            "Private courses",
        )
    with cols[2]:
        card(
            "Clear progress reporting",
            "Admins can view enrollment, quiz completion, employee progress, average progress, and active join codes from one simple dashboard",
            "Team visibility",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section alt-band home-centered fade-in">', unsafe_allow_html=True)
    page_title(
        "How your custom course comes together",
        "A simple process for turning your company’s needs into practical AI training for your team",
        centered=True,
    )
    steps = st.columns(4)
    step_data = [
        ("1", "Understand your needs", "Tell us about your team, goals, workflows, and the AI skills employees need"),
        ("2", "Design the course", "We build readings, examples, quizzes, and practice tasks around how your team works"),
        ("3", "Launch privately", "Your admin creates the course, receives a join code, and shares it with employees"),
        ("4", "Track progress", "Admins view enrollment, quiz completion, employee progress, and overall course progress"),
    ]
    for column, (number, title, text) in zip(steps, step_data):
        with column:
            st.markdown(
                f"""
                <div class="step-card">
                    <div class="step-number">{number}</div>
                    <h3>{title}</h3>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section home-centered fade-in">', unsafe_allow_html=True)
    page_title(
        "Give your team a clear way to use AI",
        "AI can support research, writing, analysis, operations, hiring, marketing, and software work. The right training helps employees use it safely, consistently, and with real purpose.",
        centered=True,
    )

    st.markdown(
        """
        <div class="home-course-card-grid">
            <div class="wide-card">
                <h3>What each course can include</h3>
                <ul>
                    <li>Reading-based lessons</li>
                    <li>Short quizzes for each lesson</li>
                    <li>Employee progress tracking</li>
                    <li>Private 6-character course join codes</li>
                    <li>Admin dashboards for managing courses and employees</li>
                    <li>Custom examples based on your team's workflows</li>
                </ul>
            </div>
            <div class="wide-card">
                <h3>Built for real workplace use</h3>
                <p>
                    Employees learn when to use AI, how to ask better questions,
                    how to protect sensitive information, and how to review AI outputs
                    before using them in real work.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <section class="cta fade-in">
            <h2>Create a custom AI course for your team</h2>
            <p>
                Tell us your goals, team size, company type, and training needs. We will shape the course around your employees and discuss details and pricing by email.
            </p>
            <a href="?page=contact" target="_self" class="light-button">Contact us</a>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_sample_courses() -> None:
    public_nav("sample_courses")
    page_title(
        "Sample course templates",
        "Open a sample course to see how a short reading and quiz flow could work for each type of team.",
        centered=True,
    )

    cards = ['<div class="sample-course-grid fade-in">']
    for idx, course in enumerate(SAMPLE_COURSES):
        course_url = sample_course_url(idx)
        thumbnail_src = sample_course_thumbnail(course["title"], idx)
        cards.append(
            dedent(
                f"""
            <a class="sample-course-tile" href="{course_url}" target="_blank" rel="noopener noreferrer">
                <img class="course-thumb-image" src="{thumbnail_src}" alt="{escape(course["title"])} thumbnail" />
                <div class="tile-body">
                    <span class="tile-kicker">Sample course</span>
                    <h3>{escape(course["title"])}</h3>
                    <p>{escape(course["description"])}</p>
                    <span class="open-pill">Open sample</span>
                </div>
            </a>
            """
            ).strip()
        )
    cards.append("</div>")
    st.markdown("\n".join(cards), unsafe_allow_html=True)


def build_sample_modules(course: dict) -> list[dict]:
    if course.get("modules"):
        return course["modules"]

    focus = course["skills"].split(",")[0].strip().lower()
    return [
        {
            "title": "Set the right use case",
            "reading": f"This lesson helps the team choose AI use cases that are worth the time. Start with repeatable work, clear inputs, and outputs that a person can review before they are used.",
            "questions": [
                {
                    "question": "What makes a good first AI use case at work?",
                    "options": [
                        "A repeatable task with output that a person can review",
                        "A task where no one checks the result",
                        "A sensitive decision that should be fully automated",
                    ],
                    "correct": "A repeatable task with output that a person can review",
                }
            ],
        },
        {
            "title": "Write useful prompts",
            "reading": f"A strong prompt explains the task, audience, constraints, and desired format. For this course, employees practice prompts tied to {focus} and then compare the output against the actual business need.",
            "questions": [
                {
                    "question": "What should a useful prompt include?",
                    "options": [
                        "Context, task, constraints, and desired format",
                        "Only one vague sentence",
                        "Private company data that is not needed",
                    ],
                    "correct": "Context, task, constraints, and desired format",
                }
            ],
        },
        {
            "title": "Review before using",
            "reading": "AI output should be treated as a draft. Employees should check facts, tone, assumptions, and missing context before using the result in client work, internal decisions, or customer communication.",
            "questions": [
                {
                    "question": "What should happen before AI output is used in real work?",
                    "options": [
                        "A person should review and verify it",
                        "It should be copied without review",
                        "It should replace company policy",
                    ],
                    "correct": "A person should review and verify it",
                }
            ],
        },
        {
            "title": "Protect sensitive information",
            "reading": "Employees need clear rules for what can and cannot be shared with AI tools. The safest workflows avoid unnecessary personal, client, financial, legal, or confidential company information.",
            "questions": [
                {
                    "question": "What is the safest approach to sensitive information?",
                    "options": [
                        "Share only what is allowed and necessary",
                        "Share everything so the answer is more detailed",
                        "Ignore internal policy when the task is urgent",
                    ],
                    "correct": "Share only what is allowed and necessary",
                }
            ],
        },
        {
            "title": "Turn habits into workflow",
            "reading": f"The final step connects AI habits to the team's normal work. Employees identify where AI can help, where human judgment is required, and how progress should be tracked after training.",
            "questions": [
                {
                    "question": "How should teams use AI after training?",
                    "options": [
                        "Build clear habits into normal workflows",
                        "Use AI randomly with no shared standards",
                        "Stop reviewing outputs once the course is finished",
                    ],
                    "correct": "Build clear habits into normal workflows",
                }
            ],
        },
    ]


def build_created_course_modules(course) -> list[dict]:
    content_template = "generic"
    if hasattr(course, "keys") and "content_template" in course.keys():
        content_template = course["content_template"]
    if content_template in COURSE_CONTENT_TEMPLATES:
        return COURSE_CONTENT_TEMPLATES[content_template]

    title = course["title"]
    company_name = course["company_name"]
    company_type = course["company_type"]
    return [
        {
            "title": "Choose practical AI use cases",
            "reading": (
                f"This lesson helps employees at {company_name} identify where AI can save time without adding risk. "
                f"For a {company_type} team, the best first use cases are repeatable, reviewable, and tied to work people already understand."
            ),
            "questions": [
                {
                    "question": "What makes a strong first AI use case at work?",
                    "options": [
                        "A repeatable task with output that a person can review",
                        "A task with no clear owner or review step",
                        "A sensitive decision that should be fully automated",
                    ],
                    "correct": "A repeatable task with output that a person can review",
                },
                {
                    "question": "Who should stay responsible for the final work product?",
                    "options": [
                        "A trained employee or manager",
                        "The AI tool by itself",
                        "No one if the prompt was detailed",
                    ],
                    "correct": "A trained employee or manager",
                },
            ],
        },
        {
            "title": "Write clear prompts",
            "reading": (
                f"A useful prompt for {title} should give context, explain the task, name any constraints, and ask for a clear format. "
                "Employees should include only the information needed for the task and leave out unnecessary private details."
            ),
            "questions": [
                {
                    "question": "What should a useful workplace prompt include?",
                    "options": [
                        "Context, task, constraints, and desired format",
                        "Only a short vague request",
                        "Private details that are not needed",
                    ],
                    "correct": "Context, task, constraints, and desired format",
                },
                {
                    "question": "What should employees avoid putting into prompts?",
                    "options": [
                        "Unnecessary sensitive information",
                        "The audience for the output",
                        "The format they want back",
                    ],
                    "correct": "Unnecessary sensitive information",
                },
            ],
        },
        {
            "title": "Review AI output carefully",
            "reading": (
                "AI output should be treated as a draft. Employees should check facts, tone, assumptions, missing context, and fit before using the output in real work."
            ),
            "questions": [
                {
                    "question": "What is the safest way to use AI for workplace tasks?",
                    "options": [
                        "Use AI as a helper, then review and verify the output before using it",
                        "Copy AI output directly into important work without checking it",
                        "Let AI replace company policy when it sounds confident",
                    ],
                    "correct": "Use AI as a helper, then review and verify the output before using it",
                },
                {
                    "question": "What should employees check before using an AI draft?",
                    "options": [
                        "Accuracy, tone, assumptions, and missing context",
                        "Only whether it is short",
                        "Whether it was generated quickly",
                    ],
                    "correct": "Accuracy, tone, assumptions, and missing context",
                },
            ],
        },
        {
            "title": "Protect company and customer information",
            "reading": (
                f"Employees in a {company_type} organization need clear rules for what can be shared with AI tools. "
                "Safe workflows avoid unnecessary personal, client, financial, legal, and confidential company information."
            ),
            "questions": [
                {
                    "question": "What is the safest approach to sensitive information?",
                    "options": [
                        "Share only what is allowed and necessary",
                        "Share everything so the answer is detailed",
                        "Ignore policy when the work is urgent",
                    ],
                    "correct": "Share only what is allowed and necessary",
                },
                {
                    "question": "What should teams use when they are unsure about a data policy?",
                    "options": [
                        "Internal guidance or a manager review",
                        "A guess based on what feels convenient",
                        "The first answer the AI tool gives",
                    ],
                    "correct": "Internal guidance or a manager review",
                },
            ],
        },
        {
            "title": "Build AI into daily workflow",
            "reading": (
                f"The final step connects AI habits to the normal work at {company_name}. "
                "Employees identify where AI can help, where human judgment is required, and how teams should keep improving after training."
            ),
            "questions": [
                {
                    "question": "How should teams use AI after training?",
                    "options": [
                        "Build clear habits into normal workflows",
                        "Use AI randomly with no shared standards",
                        "Stop reviewing outputs once the course is complete",
                    ],
                    "correct": "Build clear habits into normal workflows",
                },
                {
                    "question": "What makes AI adoption more reliable across a team?",
                    "options": [
                        "Shared standards, review habits, and clear examples",
                        "Different rules for every employee",
                        "No tracking or follow-up",
                    ],
                    "correct": "Shared standards, review habits, and clear examples",
                },
            ],
        },
    ]


def render_sample_step_progress(total_steps: int, completed_steps: int, current_step: int) -> None:
    render_step_progress(total_steps, completed_steps, current_step)


def render_sample_course_viewer() -> None:
    template_idx = get_query_int("template", 0, 0, len(SAMPLE_COURSES) - 1)
    current_step = get_query_int("step", 1, 1, 5)
    view = get_query_value("view", "reading")
    if view not in {"reading", "quiz"}:
        view = "reading"

    course = SAMPLE_COURSES[template_idx]
    modules = build_sample_modules(course)
    module = modules[current_step - 1]
    progress_key = f"sample_{template_idx}"
    completed_from_url = get_query_int("completed", 0, 0, 5)
    completed_steps = max(st.session_state.sample_course_progress.get(progress_key, 0), completed_from_url)
    st.session_state.sample_course_progress[progress_key] = completed_steps

    st.markdown('<div id="sample-course-page"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="sample-viewer fade-in">
            <a href="?page=sample_courses" target="_self" class="viewer-back">Back to sample courses</a>
            <div class="viewer-kicker">Sample course</div>
            <h1>{escape(course["title"])}</h1>
            <p>{escape(course["description"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_sample_step_progress(5, completed_steps, current_step)

    if view == "reading":
        st.markdown(
            f"""
            <div class="lesson-panel sample-lesson-panel">
                <span class="label">Step {current_step} of 5</span>
                <h2>{escape(module["title"])}</h2>
                {reading_markup(module["reading"])}
                <div class="viewer-actions">
                    <a href="{sample_course_url(template_idx, current_step, "quiz", completed_steps)}" target="_self" class="light-button">Next: quiz</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="lesson-panel sample-lesson-panel">
            <span class="label">Step {current_step} of 5</span>
            <h2>{escape(module["title"])} quiz</h2>
            <p>Answer the questions to complete this step.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    result_key = f"sample_quiz_result_{template_idx}_{current_step}"
    score_key = f"sample_quiz_score_{template_idx}_{current_step}"
    questions = get_module_questions(module)
    answers = []
    st.markdown('<div class="quiz-question-spacer"></div>', unsafe_allow_html=True)
    for index, question in enumerate(questions, start=1):
        answers.append(
            st.radio(
                f"{index}. {question['question']}",
                shuffled_answer_options(question, f"sample_quiz_options_{template_idx}_{current_step}_{index}"),
                key=f"sample_quiz_answer_{template_idx}_{current_step}_{index}",
                index=None,
            )
        )
    if st.button("Submit answers", key=f"sample_quiz_check_{template_idx}_{current_step}"):
        if any(answer is None for answer in answers):
            st.markdown(
                '<div class="quiz-status warning">Answer all questions first.</div>',
                unsafe_allow_html=True,
            )
        else:
            correct_count = sum(
                1 for answer, question in zip(answers, questions) if answer == question["correct"]
            )
            total_questions = len(questions)
            st.session_state[score_key] = f"{correct_count} of {total_questions}"
            if correct_count == total_questions:
                completed_steps = max(completed_steps, current_step)
                st.session_state.sample_course_progress[progress_key] = completed_steps
                st.session_state[result_key] = "correct"
                st.query_params["completed"] = str(completed_steps)
                st.rerun()
            else:
                st.session_state[result_key] = "incorrect"

    completed_steps = max(completed_steps, st.session_state.sample_course_progress.get(progress_key, 0))
    current_quiz_correct = st.session_state.get(result_key) == "correct"
    current_quiz_incorrect = st.session_state.get(result_key) == "incorrect"
    current_step_completed = current_step <= completed_steps
    if current_quiz_correct:
        st.markdown('<div class="quiz-status success">Correct. Step completed.</div>', unsafe_allow_html=True)
    elif current_quiz_incorrect:
        score_text = st.session_state.get(score_key, "some")
        st.markdown(
            f'<div class="quiz-status error">Not quite. You answered {escape(score_text)} correctly. Review the reading and try again.</div>',
            unsafe_allow_html=True,
        )

    if current_step_completed:
        next_link = (
            sample_course_url(template_idx, current_step + 1, "reading", completed_steps)
            if current_step < 5
            else "?page=sample_courses"
        )
        next_text = "Next reading" if current_step < 5 else "Back to sample courses"
        st.markdown(
            f"""
            <div class="viewer-actions">
                <a href="{sample_course_url(template_idx, current_step, "reading", completed_steps)}" target="_self" class="ghost-button">Back to reading</a>
                <a href="{next_link}" target="_self" class="light-button">{next_text}</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="viewer-actions">
                <a href="{sample_course_url(template_idx, current_step, "reading", completed_steps)}" target="_self" class="ghost-button">Back to reading</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_contact() -> None:
    public_nav("contact")
    page_title(
        "Contact us about a custom AI course",
        "Pricing is handled by email after we understand your company, employee count, training goals, and course requirements.",
        centered=True,
    )

    _, middle, _ = st.columns([1, 1.15, 1])
    with middle:
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Name")
            company_name = st.text_input("Company name")
            work_email = st.text_input("Work email")
            company_type = st.text_input("Company type")
            employee_count = st.text_input("Number of employees")
            requested_skills = st.text_area("What AI skills do you want your team to learn")
            additional_notes = st.text_area("Additional notes")
            submitted = st.form_submit_button("Submit request")

        if submitted:
            required = [name, company_name, work_email, company_type, employee_count, requested_skills]
            if not all(value.strip() for value in required):
                st.error("Please complete all required fields")
            elif "@" not in work_email or "." not in work_email:
                st.error("Please enter a valid work email")
            else:
                create_contact_request(
                    name=name.strip(),
                    company_name=company_name.strip(),
                    work_email=work_email.strip(),
                    company_type=company_type.strip(),
                    employee_count=employee_count.strip(),
                    requested_skills=requested_skills.strip(),
                    additional_notes=additional_notes.strip(),
                )
                st.success("Thanks. We will contact you by email to discuss your course needs.")

        st.markdown(
            """
            <div class="contact-side">
                <h3>What happens next</h3>
                <p>We review your request and contact you to discuss course goals, employee groups, delivery needs, and pricing.</p>
                <h3>What we need from you</h3>
                <p>Company type, employee count, the AI skills your team needs, and any examples of workflows the course should support.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_auth_shell(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div id="auth-page"></div>
        <div class="auth-heading fade-in">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login() -> None:
    render_auth_shell("Course platform", "Log in to access company courses")
    _, middle, _ = st.columns([1, 1.05, 1])
    with middle:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if st.session_state.account_created:
            st.success("Account created. Please log in.")
            st.session_state.account_created = False

        if submitted:
            user = get_user_by_username(username.strip())
            if user and verify_password(password, user["password_hash"]):
                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.username = user["username"]
                st.session_state.current_platform_page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.markdown('<div class="auth-link-wrap">', unsafe_allow_html=True)
        if st.button("Create an account", key="go_create_account"):
            go_platform("create_account")
        st.markdown("</div>", unsafe_allow_html=True)


def render_create_account() -> None:
    render_auth_shell("Create account", "Create a course platform account")
    _, middle, _ = st.columns([1, 1.05, 1])
    with middle:
        with st.form("create_account_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account")

        if submitted:
            clean_username = username.strip()
            if len(clean_username) < 3:
                st.error("Username must be at least 3 characters")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif get_user_by_username(clean_username):
                st.error("That username is already taken")
            else:
                create_user(clean_username, hash_password(password))
                st.session_state.account_created = True
                st.session_state.current_platform_page = "login"
                st.rerun()

        st.markdown('<div class="auth-link-wrap">', unsafe_allow_html=True)
        if st.button("Back to login", key="back_to_login"):
            go_platform("login")
        st.markdown("</div>", unsafe_allow_html=True)


def render_platform_topbar() -> None:
    left, right = st.columns([0.78, 0.22], vertical_alignment="top")
    with left:
        st.markdown('<div class="platform-brand">Course dashboard</div>', unsafe_allow_html=True)
    with right:
        with st.popover("👤", help=f"Signed in as {st.session_state.username}"):
            st.markdown(f'<div class="account-menu"><strong>Username:</strong> {escape(st.session_state.username)}</div>', unsafe_allow_html=True)
            if st.button("Change password", key="open_change_password"):
                go_platform("change_password")
            if st.button("Logout", key="account_logout"):
                logout()


def logout() -> None:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""
    st.session_state.current_platform_page = "login"
    st.session_state.selected_course_id = None
    st.session_state.selected_admin_course_id = None
    st.session_state.pending_creation_key = ""
    st.session_state.account_menu_open = False
    st.rerun()


def render_dashboard() -> None:
    render_platform_topbar()
    user_id = st.session_state.user_id
    enrolled_courses = get_enrolled_courses(user_id)
    admin_courses = get_admin_courses(user_id)

    st.markdown(
        f"""
        <section class="dashboard-hero fade-in">
            <h1>Welcome, {st.session_state.username}</h1>
            <p>Join employee courses, continue learning, or manage courses you own.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    join_col, key_col = st.columns(2, gap="large")
    with join_col:
        st.markdown('<span class="dashboard-join-panel"></span>', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Join a course</div>', unsafe_allow_html=True)
        with st.form("join_course_form"):
            join_code = st.text_input("6-character course code", max_chars=6).upper()
            submitted = st.form_submit_button("Join course")
        if submitted:
            status, message = enroll_user_in_course(user_id, join_code.strip())
            if status == "success":
                st.success(message)
                st.rerun()
            elif status == "already":
                st.info(message)
            else:
                st.error(message)

    with key_col:
        st.markdown('<span class="dashboard-join-panel"></span>', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Create a company course</div>', unsafe_allow_html=True)
        if not st.session_state.pending_creation_key:
            with st.form("creation_key_form"):
                key_value = st.text_input("15-character course creation key", max_chars=15)
                submitted = st.form_submit_button("Use creation key")
            if submitted:
                clean_key = key_value.strip()
                if len(clean_key) != 15:
                    st.error("Creation key must be exactly 15 characters")
                elif not validate_creation_key(clean_key):
                    st.error("This creation key is invalid or has already been used")
                else:
                    st.session_state.pending_creation_key = clean_key
                    st.rerun()
        else:
            render_create_course_form()

    st.markdown('<div class="section compact-section">', unsafe_allow_html=True)
    page_title("Courses you are enrolled in", "")
    if not enrolled_courses:
        st.info("You are not enrolled in any courses yet")
    else:
        for course in enrolled_courses:
            render_enrolled_course_card(course)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section compact-section">', unsafe_allow_html=True)
    page_title("Courses you manage", "")
    if not admin_courses:
        st.info("You are not managing any courses yet")
    else:
        for course in admin_courses:
            render_admin_course_card(course)
    st.markdown("</div>", unsafe_allow_html=True)


def render_create_course_form() -> None:
    st.info("Creation key accepted. Complete the course details.")
    with st.form("create_course_form"):
        company_name = st.text_input("Company name")
        title = st.text_input("Course title")
        company_type = st.text_input("Company type")
        description = st.text_area("Short course description")
        submitted = st.form_submit_button("Create course")
    cancel = st.button("Cancel course creation", key="cancel_course_creation")
    if cancel:
        st.session_state.pending_creation_key = ""
        st.rerun()
    if submitted:
        if not all([company_name.strip(), title.strip(), company_type.strip(), description.strip()]):
            st.error("Please complete all course fields")
        else:
            try:
                create_course_from_key(
                    key_value=st.session_state.pending_creation_key,
                    admin_user_id=st.session_state.user_id,
                    title=title.strip(),
                    company_name=company_name.strip(),
                    company_type=company_type.strip(),
                    description=description.strip(),
                )
                st.session_state.pending_creation_key = ""
                st.success("Course created")
                st.rerun()
            except ValueError as exc:
                st.session_state.pending_creation_key = ""
                st.error(str(exc))


def render_course_dashboard_tile(
    course,
    *,
    kicker: str,
    progress_percent: int,
    meta_lines: list[str],
    thumbnail_index: int,
) -> None:
    completed_steps = completed_steps_from_percent(progress_percent)
    active_step = None if completed_steps >= TOTAL_COURSE_STEPS else completed_steps + 1
    thumbnail_src = course_thumbnail(course["title"], thumbnail_index)
    meta_html = "".join(f"<span>{escape(line)}</span>" for line in meta_lines)
    st.markdown(
        f"""
        <div class="course-dashboard-tile">
            <img class="course-thumb-image" src="{thumbnail_src}" alt="{escape(course["title"])} thumbnail" />
            <div class="tile-body">
                <span class="tile-kicker">{escape(kicker)}</span>
                <h3>{escape(course["title"])}</h3>
                <p>{escape(course["description"])}</p>
                <div class="dashboard-card-meta">{meta_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_step_progress(TOTAL_COURSE_STEPS, completed_steps, active_step, compact=True)
    st.markdown(f'<div class="card-progress-label">{progress_percent}% complete</div>', unsafe_allow_html=True)


def render_enrolled_course_card(course) -> None:
    progress = course["progress_percent"] or 0
    with st.container(border=True):
        render_course_dashboard_tile(
            course,
            kicker="Employee course",
            progress_percent=progress,
            meta_lines=[course["company_name"]],
            thumbnail_index=course["id"],
        )
        continue_col, leave_col = st.columns(2)
        with continue_col:
            if st.button("Continue", key=f"continue_{course['id']}"):
                st.session_state.selected_course_id = course["id"]
                st.session_state.course_step = "reading"
                st.session_state.course_view_step = current_step_from_progress(progress)
                go_platform("course_view")
        with leave_col:
            st.markdown('<span class="dashboard-action-right"></span>', unsafe_allow_html=True)
            if st.button("Leave course", key=f"leave_course_{course['id']}"):
                st.session_state.pending_leave_course_id = course["id"]
                st.rerun()

        if st.session_state.pending_leave_course_id == course["id"]:
            st.markdown(
                f"""
                <div class="leave-course-panel">
                    <h3>Leave this course</h3>
                    <p>You will lose access to this course and your saved progress for it.</p>
                    <p><strong>{escape(course["title"])}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            confirm_col, cancel_col = st.columns(2)
            with confirm_col:
                if st.button("Confirm leave", key=f"confirm_leave_course_{course['id']}"):
                    left = leave_course(st.session_state.user_id, course["id"])
                    st.session_state.pending_leave_course_id = None
                    if left:
                        if st.session_state.selected_course_id == course["id"]:
                            st.session_state.selected_course_id = None
                            st.session_state.course_view_step = 1
                            st.session_state.course_step = "reading"
                        st.rerun()
                    else:
                        st.error("Could not leave that course")
            with cancel_col:
                if st.button("Cancel", key=f"cancel_leave_course_{course['id']}"):
                    st.session_state.pending_leave_course_id = None
                    st.rerun()


def render_admin_course_card(course) -> None:
    progress = course["average_progress"] or 0
    with st.container(border=True):
        render_course_dashboard_tile(
            course,
            kicker="Managed course",
            progress_percent=progress,
            meta_lines=[
                course["company_name"],
                f"Join code {course['join_code']}",
                f"{course['employee_count']} enrolled employees",
            ],
            thumbnail_index=course["id"],
        )
        view_col, manage_col = st.columns(2)
        with view_col:
            if st.button("View course", key=f"admin_view_{course['id']}"):
                st.session_state.selected_course_id = course["id"]
                st.session_state.course_step = "reading"
                st.session_state.course_view_step = 1
                go_platform("course_view")
        with manage_col:
            st.markdown('<span class="dashboard-action-right"></span>', unsafe_allow_html=True)
            if st.button("Manage course", key=f"manage_{course['id']}"):
                st.session_state.selected_admin_course_id = course["id"]
                go_platform("admin_panel")


def render_course_view() -> None:
    user_id = st.session_state.user_id
    course_id = st.session_state.selected_course_id
    course = get_course_for_learning(user_id, course_id)
    if not course:
        st.error("Course not found")
        if st.button("Back to dashboard"):
            go_platform("dashboard")
        return
    is_course_admin = int(course["admin_user_id"]) == int(user_id)

    if "course_step" not in st.session_state:
        st.session_state.course_step = "reading"

    modules = build_created_course_modules(course)
    progress = get_progress(user_id, course_id)
    percent = progress["progress_percent"] if progress else 0
    completed_steps = completed_steps_from_percent(percent)
    next_unfinished_step = current_step_from_progress(percent)
    saved_step = int(st.session_state.get("course_view_step") or next_unfinished_step)
    just_completed_quiz_key = f"course_quiz_result_{course_id}_{saved_step}"
    just_completed_quiz = (
        st.session_state.course_step == "quiz"
        and st.session_state.get(just_completed_quiz_key) == "correct"
    )
    if saved_step < next_unfinished_step and not just_completed_quiz:
        saved_step = next_unfinished_step
        st.session_state.course_view_step = saved_step
    current_step = max(1, min(TOTAL_COURSE_STEPS, saved_step))
    module = modules[current_step - 1]

    if st.session_state.course_step == "reading":
        mark_reading_viewed(user_id, course_id)

    st.markdown(
        f"""
        <div id="real-course-page"></div>
        <div class="sample-viewer course-viewer fade-in">
            <div class="viewer-kicker">{escape(course["company_name"])}</div>
            <h1>{escape(course["title"])}</h1>
            <p>{escape(course["description"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_step_progress(TOTAL_COURSE_STEPS, completed_steps, current_step)
    st.markdown(f'<div class="course-percent-label">{percent}% complete</div>', unsafe_allow_html=True)

    if st.session_state.course_step == "reading":
        st.markdown(
            f"""
            <div class="lesson-panel sample-lesson-panel fade-in">
                <span class="label">Step {current_step} of {TOTAL_COURSE_STEPS}</span>
                <h2>{escape(module["title"])}</h2>
                {reading_markup(module["reading"])}
            </div>
            """,
            unsafe_allow_html=True,
        )
        _, back_col, quiz_col, _ = st.columns([0.1, 0.4, 0.4, 0.1], gap="small")
        with back_col:
            st.markdown('<span class="course-action-left"></span>', unsafe_allow_html=True)
            if st.button("Back to dashboard", key="course_back_dashboard_reading"):
                go_platform("dashboard")
        with quiz_col:
            st.markdown('<span class="course-action-right"></span>', unsafe_allow_html=True)
            if st.button("Next: quiz", key=f"go_course_quiz_{course_id}_{current_step}"):
                st.session_state.course_step = "quiz"
                st.rerun()
    else:
        st.markdown(
            f"""
            <div class="lesson-panel sample-lesson-panel fade-in">
                <span class="label">Step {current_step} of {TOTAL_COURSE_STEPS}</span>
                <h2>{escape(module["title"])} quiz</h2>
                <p>Answer the questions to complete this step.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        result_key = f"course_quiz_result_{course_id}_{current_step}"
        score_key = f"course_quiz_score_{course_id}_{current_step}"
        questions = get_module_questions(module)
        answers = []
        st.markdown('<div class="quiz-question-spacer"></div>', unsafe_allow_html=True)
        for index, question in enumerate(questions, start=1):
            answers.append(
                st.radio(
                    f"{index}. {question['question']}",
                    shuffled_answer_options(question, f"course_quiz_options_{course_id}_{current_step}_{index}"),
                    key=f"course_quiz_{course_id}_{current_step}_{index}",
                    index=None,
                )
            )

        if st.button("Submit answers", key=f"submit_course_quiz_{course_id}_{current_step}"):
            if any(answer is None for answer in answers):
                st.markdown(
                    '<div class="quiz-status warning">Answer all questions first.</div>',
                    unsafe_allow_html=True,
                )
            else:
                correct_count = sum(
                    1 for answer, question in zip(answers, questions) if answer == question["correct"]
                )
                total_questions = len(questions)
                score = round((correct_count / total_questions) * 100)
                st.session_state[score_key] = f"{correct_count} of {total_questions}"
                if correct_count == total_questions:
                    completed_steps = max(completed_steps, current_step)
                    st.session_state.course_view_step = current_step
                    mark_course_step_completed(user_id, course_id, completed_steps, score)
                    st.session_state[result_key] = "correct"
                    st.rerun()
                else:
                    st.session_state[result_key] = "incorrect"

        latest_progress = get_progress(user_id, course_id)
        latest_percent = latest_progress["progress_percent"] if latest_progress else percent
        completed_steps = max(completed_steps, completed_steps_from_percent(latest_percent))
        current_quiz_correct = st.session_state.get(result_key) == "correct"
        current_quiz_incorrect = st.session_state.get(result_key) == "incorrect"
        current_step_completed = current_step <= completed_steps
        if current_quiz_correct:
            st.markdown('<div class="quiz-status success">Correct. Step completed.</div>', unsafe_allow_html=True)
        elif current_quiz_incorrect:
            score_text = st.session_state.get(score_key, "some")
            st.markdown(
                f'<div class="quiz-status error">Not quite. You answered {escape(score_text)} correctly. Review the reading and try again.</div>',
                unsafe_allow_html=True,
            )

        _, back_col, dashboard_col, next_col, _ = st.columns([0.1, 0.27, 0.26, 0.27, 0.1], gap="small")
        with back_col:
            st.markdown('<span class="course-action-left"></span>', unsafe_allow_html=True)
            if st.button("Back to reading", key=f"course_back_reading_{course_id}_{current_step}"):
                st.session_state.course_step = "reading"
                st.rerun()
        with dashboard_col:
            st.markdown('<span class="course-action-center"></span>', unsafe_allow_html=True)
            if st.button("Back to dashboard", key=f"course_back_dashboard_quiz_{course_id}_{current_step}"):
                go_platform("dashboard")
        with next_col:
            st.markdown('<span class="course-action-right"></span>', unsafe_allow_html=True)
            if (current_step_completed or is_course_admin) and current_step < TOTAL_COURSE_STEPS:
                if st.button("Next reading", key=f"course_next_reading_{course_id}_{current_step}"):
                    st.session_state.course_view_step = current_step + 1
                    st.session_state.course_step = "reading"
                    st.rerun()


def render_admin_panel() -> None:
    course_id = st.session_state.selected_admin_course_id
    course, employees = get_admin_course(st.session_state.user_id, course_id)
    if not course:
        st.error("Managed course not found")
        if st.button("Back to dashboard"):
            go_platform("dashboard")
        return

    st.markdown('<div id="admin-panel-page"></div>', unsafe_allow_html=True)
    top_left, top_right = st.columns([0.75, 0.25])
    with top_left:
        st.markdown(f'<div class="viewer-title">Manage {course["title"]}</div>', unsafe_allow_html=True)
    with top_right:
        st.markdown('<div class="admin-back-target"></div>', unsafe_allow_html=True)
        if st.button("Back to dashboard"):
            go_platform("dashboard")

    st.markdown(
        f"""
        <div class="admin-summary fade-in">
            <h3>Course details</h3>
            <p><strong>Company:</strong> {course["company_name"]}</p>
            <p><strong>Company type:</strong> {course["company_type"]}</p>
            <p><strong>Join code:</strong> {course["join_code"]}</p>
            <p><strong>Average course progress:</strong> {course["average_progress"]}%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Regenerate join code"):
        new_code = regenerate_join_code(st.session_state.user_id, course_id)
        st.success(f"New join code: {new_code}")
        st.rerun()

    with st.expander("Edit course title and description"):
        with st.form("edit_course_form"):
            title = st.text_input("Course title", value=course["title"])
            description = st.text_area("Short course description", value=course["description"])
            submitted = st.form_submit_button("Save changes")
        if submitted:
            if not title.strip() or not description.strip():
                st.error("Title and description are required")
            else:
                update_course_details(st.session_state.user_id, course_id, title.strip(), description.strip())
                st.success("Course updated")
                st.rerun()

    with st.expander("Delete course"):
        st.markdown(
            f"""
            <div class="delete-course-panel">
                <h3>Delete this course</h3>
                <p>This removes the course, employee enrollments, and saved progress from this prototype database.</p>
                <p>Type <strong>{escape(course["title"])}</strong> to confirm.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        confirmation = st.text_input(
            "Confirm course title",
            key=f"delete_course_confirm_{course_id}",
            placeholder=course["title"],
        )
        if st.button("Delete course", key=f"delete_course_{course_id}"):
            if confirmation.strip() != course["title"]:
                st.error("Type the exact course title before deleting")
            else:
                deleted = delete_admin_course(st.session_state.user_id, course_id)
                if deleted:
                    st.session_state.selected_admin_course_id = None
                    st.session_state.selected_course_id = None
                    st.session_state.course_view_step = 1
                    st.session_state.course_step = "reading"
                    st.success("Course deleted")
                    go_platform("dashboard")
                else:
                    st.error("Could not delete that course")

    st.markdown('<div class="section compact-section">', unsafe_allow_html=True)
    page_title("Employee list", "")
    if not employees:
        st.info("No employees have joined this course yet")
    else:
        search_term = st.text_input(
            "Search employees",
            key=f"employee_search_{course_id}",
            placeholder="Search by username",
        ).strip().lower()
        filtered_employees = [
            employee for employee in employees if not search_term or search_term in employee["username"].lower()
        ]
        if not filtered_employees:
            st.info("No employees match that search")
        for employee in filtered_employees:
            quiz_status = "Completed" if employee["quiz_completed"] else "Not completed"
            progress_percent = employee["progress_percent"] or 0
            completed_steps = completed_steps_from_percent(progress_percent)
            active_step = None if completed_steps >= TOTAL_COURSE_STEPS else completed_steps + 1
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="employee-manage-card">
                        <div>
                            <h3>{escape(employee["username"])}</h3>
                            <p>Quiz status: {quiz_status}</p>
                        </div>
                        <div class="employee-progress-percent">{progress_percent}% complete</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                render_step_progress(TOTAL_COURSE_STEPS, completed_steps, active_step, compact=True)
                if st.button("Remove employee", key=f"remove_employee_{course_id}_{employee['user_id']}"):
                    removed = remove_employee_from_course(
                        st.session_state.user_id,
                        course_id,
                        employee["user_id"],
                    )
                    if removed:
                        st.success(f"{employee['username']} was removed from this course")
                        st.rerun()
                    else:
                        st.error("Could not remove that employee")
    st.markdown("</div>", unsafe_allow_html=True)


def render_change_password() -> None:
    render_platform_topbar()
    st.markdown('<div id="change-password-page"></div>', unsafe_allow_html=True)
    page_title("Change password", "Update the password for your course platform account", centered=True)

    with st.form("change_password_form"):
        current_password = st.text_input("Current password", type="password")
        new_password = st.text_input("New password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Change password")

    if submitted:
        user = get_user_by_id(st.session_state.user_id)
        if not user or not verify_password(current_password, user["password_hash"]):
            st.error("Current password is incorrect")
        elif len(new_password) < 8:
            st.error("New password must be at least 8 characters")
        elif new_password != confirm_password:
            st.error("New passwords do not match")
        else:
            change_user_password(st.session_state.user_id, hash_password(new_password))
            st.success("Password changed")

    st.markdown('<span class="change-password-back-action"></span>', unsafe_allow_html=True)
    if st.button("Back to dashboard", key="password_back_dashboard"):
        go_platform("dashboard")


def render_course_platform() -> None:
    if not st.session_state.logged_in:
        if st.session_state.current_platform_page == "create_account":
            render_create_account()
        else:
            st.session_state.current_platform_page = "login"
            render_login()
        return

    platform_page = st.session_state.current_platform_page
    if platform_page == "course_view":
        render_course_view()
    elif platform_page == "admin_panel":
        render_admin_panel()
    elif platform_page == "change_password":
        render_change_password()
    else:
        st.session_state.current_platform_page = "dashboard"
        render_dashboard()


def main() -> None:
    init_session_state()
    page = get_query_page()

    if page == "courses":
        render_course_platform()
    elif page == "sample_course":
        render_sample_course_viewer()
    elif page == "sample_courses":
        render_sample_courses()
    elif page == "contact":
        render_contact()
    else:
        if page != "home":
            set_public_page("home")
        render_home()


if __name__ == "__main__":
    main()
