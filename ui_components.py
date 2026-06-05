import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
        <style>
            :root {
                --text: #111113;
                --muted: #676b73;
                --soft: #f7f8fa;
                --softer: #fbfbfc;
                --line: #e8eaee;
                --line-strong: #d8dbe1;
                --accent: #eef1f5;
            }

            html, body, [class*="css"] {
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                color: var(--text) !important;
                background: #ffffff !important;
            }

            .stApp {
                background: #ffffff !important;
                color: var(--text) !important;
            }

            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            [data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stDecoration"] {
                background: #ffffff !important;
                color: var(--text) !important;
            }

            #MainMenu, footer, header {
                visibility: hidden;
            }

            .block-container {
                max-width: 1160px;
                padding-top: 1.4rem;
                padding-left: 1rem;
                padding-right: 1rem;
                padding-bottom: 4rem;
            }

            a {
                color: var(--text);
                text-decoration: none !important;
            }

            h1,
            h2,
            h3,
            h4,
            h5,
            h6,
            label {
                color: var(--text) !important;
            }

            .topnav {
                position: sticky;
                top: 0;
                z-index: 50;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                padding: 0.8rem 1rem;
                margin-bottom: 3rem;
                background: rgba(255, 255, 255, 0.92);
                backdrop-filter: blur(18px);
                border: 1px solid var(--line);
                border-radius: 999px;
            }

            .brand {
                font-weight: 720;
                letter-spacing: 0;
                white-space: nowrap;
            }

            .navlinks {
                display: flex;
                align-items: center;
                justify-content: flex-end;
                gap: 0.25rem;
                flex-wrap: wrap;
            }

            .navlinks a {
                padding: 0.55rem 0.85rem;
                border-radius: 999px;
                color: var(--muted);
                font-size: 0.94rem;
                transition: background 180ms ease, color 180ms ease, transform 180ms ease;
            }

            .navlinks a:hover,
            .navlinks a.active {
                background: var(--soft);
                color: var(--text);
                transform: translateY(-1px);
            }

            .hero {
                min-height: 520px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 4.25rem 1rem 4.75rem;
            }

            .hero-kicker {
                color: var(--muted);
                font-size: 1rem;
                margin-bottom: 1.1rem;
            }

            .hero h1 {
                max-width: 1040px;
                font-size: clamp(2.4rem, 6vw, 5rem);
                line-height: 1.02;
                letter-spacing: 0;
                margin: 0;
                font-weight: 760;
                text-wrap: balance;
            }

            .hero p {
                max-width: 800px;
                margin: 1.35rem auto 0;
                color: var(--muted);
                font-size: 1.1rem;
                line-height: 1.65;
                text-wrap: balance;
            }

            .hero-actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 0.75rem;
                margin-top: 2rem;
            }

            .light-button,
            .ghost-button {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-height: 42px;
                padding: 0.72rem 1rem;
                border-radius: 999px;
                border: 1px solid var(--line-strong);
                background: #ffffff !important;
                color: var(--text);
                font-weight: 640;
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
                text-decoration: none !important;
            }

            a.light-button,
            a.ghost-button,
            .stMarkdownContainer a.light-button,
            .stMarkdownContainer a.ghost-button {
                color: var(--text) !important;
                -webkit-text-fill-color: var(--text) !important;
            }

            .light-button *,
            .ghost-button * {
                color: var(--text) !important;
                text-decoration: none !important;
            }

            .light-button {
                background: #ffffff !important;
            }

            .light-button:hover,
            .ghost-button:hover {
                transform: translateY(-1px);
                border-color: #c8ccd4;
                background: #f9fafb;
            }

            .section {
                padding: 3.8rem 0;
            }

            .compact-section {
                padding: 2rem 0 0;
            }

            .alt-band {
                background: linear-gradient(180deg, #ffffff 0%, #f8f9fb 100%);
                border-top: 1px solid var(--line);
                border-bottom: 1px solid var(--line);
                margin-left: calc((100% - 100vw) / 2);
                margin-right: calc((100% - 100vw) / 2);
                padding-left: max(1rem, calc((100vw - 1160px) / 2));
                padding-right: max(1rem, calc((100vw - 1160px) / 2));
            }

            .section-title {
                max-width: 760px;
                margin-bottom: 1.6rem;
            }

            .home-centered .section-title,
            .section-title.center-title {
                margin-left: auto;
                margin-right: auto;
                text-align: center;
            }

            .section-title h2 {
                font-size: clamp(1.9rem, 4vw, 3.15rem);
                line-height: 1.08;
                letter-spacing: 0;
                margin: 0 0 0.8rem;
                font-weight: 720;
                text-wrap: balance;
            }

            .section-title p {
                color: var(--muted);
                font-size: 1.05rem;
                line-height: 1.65;
                margin: 0;
                text-wrap: balance;
            }

            .soft-card,
            .wide-card,
            .step-card,
            .preview-panel,
            .contact-side,
            .lesson-panel,
            .admin-summary {
                background: var(--softer);
                border: 1px solid var(--line);
                border-radius: 22px;
                padding: 1.35rem;
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
            }

            .soft-card:hover,
            .step-card:hover,
            .wide-card:hover {
                transform: translateY(-3px);
                border-color: var(--line-strong);
                background: #ffffff;
            }

            .home-course-card-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                align-items: stretch;
                gap: 1rem;
            }

            .home-course-card-grid .wide-card {
                height: 100%;
                min-height: 100%;
            }

            .soft-card h3,
            .wide-card h3,
            .step-card h3,
            .contact-side h3,
            .course-card h3,
            .admin-summary h3 {
                margin: 0 0 0.65rem;
                font-size: 1.15rem;
                letter-spacing: 0;
            }

            .soft-card p,
            .wide-card p,
            .step-card p,
            .contact-side p,
            .course-card p,
            .template-card p,
            .preview-panel p,
            .lesson-panel p,
            .admin-summary p {
                color: var(--muted);
                line-height: 1.62;
                margin: 0.35rem 0;
            }

            .wide-card ul {
                margin: 0.5rem 0 0;
                padding-left: 1.2rem;
                color: var(--muted);
                line-height: 1.75;
            }

            .card-meta,
            .label {
                display: inline-block;
                margin-bottom: 0.7rem;
                color: #5f6670;
                font-size: 0.82rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0;
            }

            .step-number {
                width: 34px;
                height: 34px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: #ffffff;
                border: 1px solid var(--line);
                margin-bottom: 1rem;
                color: var(--muted);
                font-weight: 700;
            }

            .cta {
                text-align: center;
                padding: 4rem 1rem;
                border: 1px solid var(--line);
                border-radius: 28px;
                background: #fafbfc;
            }

            .cta h2 {
                margin: 0;
                font-size: clamp(2rem, 5vw, 3.8rem);
                line-height: 1.05;
                letter-spacing: 0;
            }

            .cta p {
                color: var(--muted);
                max-width: 620px;
                margin: 1rem auto 1.5rem;
                line-height: 1.6;
            }

            .template-card h3 {
                margin: 0 0 0.55rem;
                font-size: 1.25rem;
            }

            .sample-course-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 1rem;
                margin-top: 1.2rem;
            }

            .sample-course-tile {
                min-height: 470px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                gap: 0;
                padding: 0;
                overflow: hidden;
                border: 1px solid var(--line);
                border-radius: 24px;
                background: #fbfbfc;
                color: var(--text);
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
            }

            a.sample-course-tile,
            .stMarkdownContainer a.sample-course-tile {
                color: var(--text) !important;
                -webkit-text-fill-color: var(--text) !important;
            }

            .sample-course-tile,
            .sample-course-tile * {
                text-decoration: none !important;
            }

            .sample-course-tile:hover {
                transform: translateY(-3px);
                border-color: var(--line-strong);
                background: #ffffff;
            }

            .course-thumb-image {
                width: 100%;
                height: 205px;
                display: block;
                object-fit: cover;
                border-bottom: 1px solid var(--line);
                background: #f7f8fa;
            }

            .tile-body {
                min-height: 245px;
                display: flex;
                flex-direction: column;
                gap: 0.72rem;
                padding: 1.25rem;
                text-align: left;
            }

            .sample-course-tile h3,
            .course-dashboard-tile h3 {
                font-size: 1.28rem;
                line-height: 1.22;
                margin: 0;
                text-wrap: balance;
                color: var(--text) !important;
            }

            .sample-course-tile p,
            .sample-course-tile span,
            .course-dashboard-tile p,
            .course-dashboard-tile span {
                color: var(--muted);
                line-height: 1.55;
            }

            .course-dashboard-tile p {
                margin: 0;
            }

            .tile-kicker {
                display: block;
                font-size: 0.78rem;
                font-weight: 740;
                text-transform: uppercase;
                letter-spacing: 0;
            }

            .tile-meta {
                display: grid;
                gap: 0.18rem;
            }

            .tile-meta strong {
                color: var(--text);
                font-size: 0.92rem;
            }

            .open-pill {
                width: fit-content;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.55rem 0.8rem;
                border-radius: 999px;
                border: 1px solid var(--line-strong);
                background: #ffffff;
                color: var(--text) !important;
                font-weight: 680;
                margin-top: auto;
            }

            .course-dashboard-tile {
                overflow: hidden;
                border-radius: 20px;
                background: #fbfbfc;
            }

            .course-dashboard-tile .tile-body {
                min-height: 220px;
            }

            .dashboard-card-meta {
                display: grid;
                gap: 0.28rem;
                margin-top: auto;
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.45;
            }

            .dashboard-card-meta span {
                color: var(--muted);
            }

            .card-progress {
                margin: 1rem auto 0.45rem;
                max-width: 100%;
            }

            .card-progress .progress-circle {
                width: 30px;
                height: 30px;
                flex-basis: 30px;
                font-size: 0.82rem;
            }

            .card-progress .progress-line {
                flex-basis: 34px;
            }

            .card-progress-label,
            .course-percent-label {
                color: var(--muted);
                font-size: 0.92rem;
                font-weight: 640;
            }

            .card-progress-label {
                margin-bottom: 0.8rem;
            }

            .dashboard-action-right {
                display: block;
                height: 0;
                overflow: hidden;
            }

            [data-testid="stElementContainer"]:has(.dashboard-action-right),
            [data-testid="stMarkdown"]:has(.dashboard-action-right),
            [data-testid="stMarkdownContainer"]:has(.dashboard-action-right),
            [data-testid="stMarkdownContainer"]:has(.dashboard-action-right) p {
                height: 0 !important;
                min-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }

            [data-testid="stColumn"]:has(.dashboard-action-right) [data-testid="stElementContainer"]:has(.stButton) {
                width: 100% !important;
                max-width: 100% !important;
                display: flex !important;
                justify-content: flex-end !important;
            }

            [data-testid="stColumn"]:has(.dashboard-action-right) .stButton {
                width: 100% !important;
                display: flex !important;
                justify-content: flex-end !important;
            }

            [data-testid="stColumn"]:has(.dashboard-action-right) .stButton > button {
                width: auto !important;
                margin-left: auto !important;
            }

            .course-percent-label {
                max-width: 900px;
                margin: -0.8rem auto 1.2rem;
                text-align: center;
            }

            .sample-viewer {
                max-width: 900px;
                margin: 0 auto;
                padding-top: 2.5rem;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .sample-viewer h1 {
                font-size: clamp(2.2rem, 5vw, 4rem);
                line-height: 1.08;
                letter-spacing: 0;
                margin: 0.55rem 0 0.7rem;
                width: min(100%, 820px);
                margin-left: auto;
                margin-right: auto;
                text-align: center;
                text-wrap: balance;
            }

            .sample-viewer p {
                max-width: 760px;
                margin: 0 auto;
                color: var(--muted);
                line-height: 1.65;
                text-wrap: balance;
            }

            .viewer-kicker,
            .viewer-back {
                color: var(--muted);
                font-size: 0.92rem;
                font-weight: 680;
            }

            .viewer-kicker {
                display: block;
                width: 100%;
                text-align: center;
            }

            .viewer-back {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-height: 38px;
                padding: 0.58rem 0.9rem;
                margin-bottom: 1.2rem;
                border: 1px solid var(--line-strong);
                border-radius: 999px;
                background: #ffffff;
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
            }

            a.viewer-back,
            .stMarkdownContainer a.viewer-back {
                color: var(--text) !important;
                -webkit-text-fill-color: var(--text) !important;
                text-decoration: none !important;
            }

            .viewer-back:hover {
                transform: translateY(-1px);
                border-color: #c8ccd4;
                background: #f9fafb;
            }

            .sample-progress {
                max-width: 900px;
                margin: 1.6rem auto 1.8rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .progress-circle {
                width: 42px;
                height: 42px;
                flex: 0 0 42px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                border: 1px solid #d5d9e0;
                background: #ffffff;
                color: #747b86;
                font-weight: 740;
            }

            .progress-circle.completed {
                background: #eef1f5;
                border-color: #aeb6c2;
                color: var(--text);
            }

            .progress-circle.active {
                background: #ffffff;
                border-color: #9ca6b4;
                color: var(--text);
                box-shadow: 0 0 0 4px rgba(210, 215, 224, 0.38);
            }

            .progress-line {
                height: 0;
                flex: 1 1 70px;
                border-top: 2px dotted #cfd4dc;
            }

            .progress-line.completed {
                border-top-style: solid;
                border-color: #9da7b5;
            }

            .sample-lesson-panel {
                max-width: 900px;
                margin: 0 auto;
                text-align: left;
            }

            .sample-lesson-panel h2 {
                font-size: clamp(1.8rem, 3vw, 2.55rem);
                line-height: 1.12;
                text-wrap: balance;
            }

            .sample-lesson-panel p {
                font-size: 1.04rem;
            }

            .viewer-actions {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: flex-start;
                gap: 0.75rem;
                margin-top: 1.25rem;
            }

            .template-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }

            .preview-panel {
                margin-top: 1rem;
                margin-bottom: 1rem;
            }

            .preview-panel h4,
            .lesson-panel h2 {
                margin: 0 0 0.7rem;
                letter-spacing: 0;
            }

            .quiz-status {
                border-radius: 14px;
                padding: 0.85rem 1rem;
                margin: 0.9rem 0 0.2rem;
                font-weight: 650;
                line-height: 1.45;
            }

            .quiz-status.success {
                background: #eefbf3;
                border: 1px solid #badfc8;
                color: #17633a;
            }

            .quiz-status.error {
                background: #fff3f3;
                border: 1px solid #efc7c7;
                color: #8f2f2f;
            }

            .quiz-status.warning {
                background: #fff8df;
                border: 1px solid #ead38a;
                color: #6d5212;
            }

            [data-testid="stAlert"] {
                border-radius: 16px !important;
                border: 1px solid var(--line-strong) !important;
                background: #ffffff !important;
                color: var(--text) !important;
                box-shadow: none !important;
                margin: 0.75rem 0 !important;
            }

            [data-testid="stAlert"] > div {
                background: #ffffff !important;
                color: var(--text) !important;
            }

            [data-testid="stAlert"] *,
            [data-testid="stAlert"] p,
            [data-testid="stAlert"] span,
            [data-testid="stAlert"] div,
            [data-testid="stAlert"] [data-testid="stMarkdownContainer"],
            [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
                color: var(--text) !important;
                opacity: 1 !important;
            }

            [data-testid="stAlert"] svg,
            [data-testid="stAlert"] svg * {
                color: #555b64 !important;
                fill: #555b64 !important;
                stroke: #555b64 !important;
                opacity: 1 !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentError"]),
            [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) > [data-testid="stAlertContainer"] {
                background: #fff3f3 !important;
                border-color: #efc7c7 !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) *,
            [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) svg,
            [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) svg * {
                color: #8f2f2f !important;
                fill: #8f2f2f !important;
                stroke: #8f2f2f !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]),
            [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) > [data-testid="stAlertContainer"] {
                background: #f1f7ff !important;
                border-color: #bed7f2 !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) *,
            [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) svg,
            [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) svg * {
                color: #214f7a !important;
                fill: #214f7a !important;
                stroke: #214f7a !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]),
            [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) > [data-testid="stAlertContainer"] {
                background: #eefbf3 !important;
                border-color: #badfc8 !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) *,
            [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) svg,
            [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) svg * {
                color: #17633a !important;
                fill: #17633a !important;
                stroke: #17633a !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]),
            [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) > [data-testid="stAlertContainer"] {
                background: #fff8df !important;
                border-color: #ead38a !important;
            }

            [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) *,
            [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) svg,
            [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) svg * {
                color: #6d5212 !important;
                fill: #6d5212 !important;
                stroke: #6d5212 !important;
            }

            [data-testid="stMain"]:has(#sample-course-page) [data-testid="stRadio"],
            [data-testid="stMain"]:has(#real-course-page) [data-testid="stRadio"],
            [data-testid="stMain"]:has(#sample-course-page) .stButton,
            [data-testid="stMain"]:has(#real-course-page) .stButton,
            [data-testid="stMain"]:has(#sample-course-page) .quiz-status,
            [data-testid="stMain"]:has(#real-course-page) .quiz-status,
            [data-testid="stMain"]:has(#sample-course-page) .viewer-actions,
            [data-testid="stMain"]:has(#real-course-page) .viewer-actions {
                width: 100% !important;
                max-width: 900px !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            [data-testid="stMain"]:has(#sample-course-page) .quiz-question-spacer,
            [data-testid="stMain"]:has(#real-course-page) .quiz-question-spacer {
                height: 1.25rem;
                max-width: 900px;
                margin: 0 auto;
            }

            [data-testid="stMain"]:has(#sample-course-page) .stElementContainer:has([data-testid="stRadio"]),
            [data-testid="stMain"]:has(#real-course-page) .stElementContainer:has([data-testid="stRadio"]),
            [data-testid="stMain"]:has(#sample-course-page) .stElementContainer:has(.stButton),
            [data-testid="stMain"]:has(#real-course-page) .stElementContainer:has(.stButton) {
                width: 100% !important;
                max-width: 900px !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            [data-testid="stMain"]:has(#sample-course-page) .stButton,
            [data-testid="stMain"]:has(#real-course-page) .stButton {
                display: flex !important;
                justify-content: flex-start !important;
            }

            [data-testid="stMain"]:has(#sample-course-page) .stButton > button,
            [data-testid="stMain"]:has(#real-course-page) .stButton > button {
                width: auto !important;
            }

            .course-action-left,
            .course-action-center,
            .course-action-right {
                display: block;
                height: 0;
                overflow: hidden;
            }

            [data-testid="stMain"]:has(#real-course-page) .stColumn:has(.course-action-left) .stButton {
                width: 100% !important;
                max-width: none !important;
                display: flex !important;
                justify-content: flex-start !important;
            }

            [data-testid="stMain"]:has(#real-course-page) .stColumn:has(.course-action-center) .stButton {
                width: 100% !important;
                max-width: none !important;
                display: flex !important;
                justify-content: center !important;
            }

            [data-testid="stMain"]:has(#real-course-page) .stColumn:has(.course-action-right) .stButton {
                width: 100% !important;
                max-width: none !important;
                display: flex !important;
                justify-content: flex-end !important;
            }

            [data-testid="stMain"]:has(#real-course-page) .stColumn:has(.course-action-left) .stElementContainer,
            [data-testid="stMain"]:has(#real-course-page) .stColumn:has(.course-action-center) .stElementContainer,
            [data-testid="stMain"]:has(#real-course-page) .stColumn:has(.course-action-right) .stElementContainer {
                max-width: 100% !important;
            }

            .contact-side {
                position: sticky;
                top: 6rem;
                margin-top: 1rem;
            }

            .auth-heading {
                text-align: center;
                padding: 5rem 0 1.5rem;
            }

            .auth-heading h1 {
                font-size: clamp(2.25rem, 5vw, 4.2rem);
                line-height: 1.05;
                letter-spacing: 0;
                margin: 0;
                color: var(--text) !important;
            }

            .auth-heading p {
                color: var(--muted) !important;
                margin-top: 0.75rem;
            }

            .auth-link-wrap {
                display: flex;
                justify-content: center;
                margin-top: 0.8rem;
            }

            .stFormSubmitButton {
                display: flex;
                justify-content: center;
            }

            [data-testid="stMain"]:has(#auth-page) .stElementContainer:has(.stFormSubmitButton),
            [data-testid="stMain"]:has(#auth-page) .stElementContainer:has(.stButton) {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
            }

            [data-testid="stMain"]:has(#auth-page) .stFormSubmitButton,
            [data-testid="stMain"]:has(#auth-page) .stButton {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
            }

            [data-testid="stMain"]:has(#auth-page) .stButton > button,
            [data-testid="stMain"]:has(#auth-page) .stFormSubmitButton > button {
                width: auto !important;
            }

            #change-password-page {
                display: block;
                height: 0;
                overflow: hidden;
            }

            .change-password-back-action {
                display: block;
                height: 0;
                overflow: hidden;
            }

            [data-testid="stElementContainer"]:has(.change-password-back-action),
            [data-testid="stMarkdown"]:has(.change-password-back-action),
            [data-testid="stMarkdownContainer"]:has(.change-password-back-action),
            [data-testid="stMarkdownContainer"]:has(.change-password-back-action) p {
                height: 0 !important;
                min-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }

            [data-testid="stMain"]:has(#change-password-page) .section-title {
                max-width: 680px;
                margin-left: auto;
                margin-right: auto;
                padding-top: 3rem;
                text-align: center;
            }

            [data-testid="stMain"]:has(#change-password-page) [data-testid="stForm"],
            [data-testid="stMain"]:has(#change-password-page) [data-testid="stAlert"],
            [data-testid="stMain"]:has(#change-password-page) .stElementContainer:has(.stFormSubmitButton) {
                width: min(100%, 460px) !important;
                max-width: 460px !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            [data-testid="stMain"]:has(#change-password-page) [data-testid="stElementContainer"]:has(.change-password-back-action)
            + [data-testid="stElementContainer"]:has(.stButton) {
                width: min(100%, 460px) !important;
                max-width: 460px !important;
                margin-left: auto !important;
                margin-right: auto !important;
                display: flex !important;
                justify-content: center !important;
            }

            [data-testid="stMain"]:has(#change-password-page) [data-testid="stForm"] {
                border: 0 !important;
                background: transparent !important;
                padding: 0 !important;
            }

            [data-testid="stMain"]:has(#change-password-page) .stFormSubmitButton,
            [data-testid="stMain"]:has(#change-password-page) .stButton {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
            }

            [data-testid="stMain"]:has(#change-password-page) .stButton > button,
            [data-testid="stMain"]:has(#change-password-page) .stFormSubmitButton > button {
                width: auto !important;
            }

            .platform-brand {
                font-size: 1.12rem;
                font-weight: 720;
                padding-top: 0.35rem;
            }

            .dashboard-hero {
                padding: 3rem 0 2rem;
            }

            .dashboard-hero h1,
            .viewer-title {
                font-size: clamp(2rem, 5vw, 3.35rem);
                line-height: 1.08;
                letter-spacing: 0;
                margin: 0;
                font-weight: 730;
            }

            .dashboard-hero p {
                color: var(--muted);
                margin-top: 0.7rem;
                font-size: 1.05rem;
            }

            .panel-title {
                font-weight: 720;
                margin-bottom: 0.65rem;
                font-size: 1.08rem;
            }

            .dashboard-join-panel {
                display: block;
                height: 0;
                overflow: hidden;
            }

            [data-testid="stElementContainer"]:has(.dashboard-join-panel),
            [data-testid="stMarkdown"]:has(.dashboard-join-panel),
            [data-testid="stMarkdownContainer"]:has(.dashboard-join-panel),
            [data-testid="stMarkdownContainer"]:has(.dashboard-join-panel) p {
                height: 0 !important;
                min-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }

            [data-testid="stColumn"]:has(.dashboard-join-panel) [data-testid="stForm"] {
                border: 0 !important;
                background: transparent !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            [data-testid="stColumn"]:has(.dashboard-join-panel) [data-testid="stForm"] > div {
                padding-left: 0 !important;
                padding-right: 0 !important;
                margin-left: 0 !important;
                margin-right: 0 !important;
            }

            .course-card span {
                color: var(--muted);
                font-size: 0.95rem;
            }

            .account-menu {
                border: 1px solid var(--line);
                background: #ffffff;
                border-radius: 16px;
                color: var(--text);
                padding: 0.8rem 0.9rem;
                margin: 0 0 0.5rem;
            }

            [data-testid="stPopover"] {
                width: 100% !important;
                display: flex;
                justify-content: flex-end;
            }

            [data-testid="stElementContainer"]:has([data-testid="stPopover"]),
            [data-testid="stLayoutWrapper"]:has([data-testid="stPopover"]) {
                width: 100% !important;
                display: flex !important;
                justify-content: flex-end !important;
            }

            [data-testid="stPopover"] button,
            [data-testid="stPopover"] > button,
            [data-testid="stPopover"] button[kind],
            [data-testid="stPopover"] button[data-baseweb] {
                width: 50px;
                height: 44px;
                min-width: 50px;
                min-height: 44px;
                padding: 0;
                border-radius: 13px;
                background: #ffffff !important;
                border: 1px solid var(--line-strong) !important;
                color: var(--text) !important;
                box-shadow: none !important;
            }

            [data-testid="stPopover"] button:hover,
            [data-testid="stPopover"] > button:hover {
                background: #f8f9fb !important;
                transform: translateY(-1px);
            }

            [data-testid="stPopover"] button *,
            [data-testid="stPopover"] > button * {
                color: var(--text) !important;
                fill: var(--text) !important;
            }

            [data-baseweb="popover"],
            div[role="dialog"] {
                background-color: #ffffff !important;
                border: 1px solid var(--line) !important;
                border-radius: 18px !important;
                box-shadow: 0 10px 32px rgba(17, 17, 19, 0.08) !important;
                color: var(--text) !important;
            }

            [data-baseweb="popover"] > div,
            [data-baseweb="popover"] [data-testid="stVerticalBlock"],
            [data-baseweb="popover"] [data-testid="stVerticalBlock"] > div,
            div[role="dialog"] > div {
                background-color: #ffffff !important;
                color: var(--text) !important;
                border-color: var(--line) !important;
            }

            [data-baseweb="popover"] p,
            [data-baseweb="popover"] span,
            [data-baseweb="popover"] strong,
            div[role="dialog"] p,
            div[role="dialog"] span,
            div[role="dialog"] strong {
                background: transparent !important;
                color: var(--text) !important;
            }

            [data-baseweb="popover"] .stButton,
            div[role="dialog"] .stButton {
                margin: 0 !important;
                width: 100% !important;
            }

            [data-baseweb="popover"] [data-testid="stVerticalBlock"],
            div[role="dialog"] [data-testid="stVerticalBlock"] {
                gap: 0.6rem !important;
            }

            [data-baseweb="popover"] .stElementContainer:has(.stButton),
            div[role="dialog"] .stElementContainer:has(.stButton) {
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
            }

            [data-baseweb="popover"] .stButton > button,
            div[role="dialog"] .stButton > button {
                width: 100% !important;
                justify-content: center;
                background: #f6f7f9 !important;
                border: 1px solid var(--line-strong) !important;
                color: var(--text) !important;
                box-shadow: none !important;
            }

            [data-baseweb="popover"] .stButton > button:hover,
            div[role="dialog"] .stButton > button:hover {
                background: #ffffff !important;
                color: var(--text) !important;
            }

            [data-testid="stExpander"],
            [data-testid="stExpander"] details,
            [data-testid="stExpander"] summary,
            [data-testid="stExpander"] summary:hover,
            [data-testid="stExpander"] summary:focus,
            [data-testid="stExpander"] summary:active,
            [data-testid="stExpanderDetails"],
            details,
            details summary,
            details summary:hover,
            details summary:focus,
            details summary:active {
                background: #ffffff !important;
                color: var(--text) !important;
                border-color: var(--line) !important;
                box-shadow: none !important;
            }

            [data-testid="stExpander"] *,
            details summary *,
            [data-testid="stExpanderDetails"] * {
                color: var(--text) !important;
            }

            details:not([open]) [data-testid="stExpanderDetails"],
            details:not([open]) [data-testid="stExpanderDetails"] * {
                display: none !important;
                height: 0 !important;
                min-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }

            [data-testid="stMain"]:has(#admin-panel-page) .stElementContainer:has(.admin-back-target),
            [data-testid="stMain"]:has(#admin-panel-page) .stElementContainer:has(.admin-back-target) + .stElementContainer {
                width: 100% !important;
                max-width: 100% !important;
                display: flex !important;
                justify-content: flex-end !important;
            }

            [data-testid="stMain"]:has(#admin-panel-page) .stColumn:has(.admin-back-target) [data-testid="stVerticalBlock"],
            [data-testid="stMain"]:has(#admin-panel-page) .stColumn:has(.admin-back-target) [data-testid="stElementContainer"] {
                width: 100% !important;
                max-width: 100% !important;
            }

            [data-testid="stMain"]:has(#admin-panel-page) .stColumn:has(.admin-back-target) .stButton {
                width: 100% !important;
                display: flex !important;
                justify-content: flex-end !important;
            }

            [data-testid="stMain"]:has(#admin-panel-page) .stColumn:has(.admin-back-target) .stButton > button {
                width: auto !important;
                margin-left: auto !important;
            }

            [data-testid="stMain"]:has(#admin-panel-page) .stElementContainer:has(.admin-back-target) + .stElementContainer .stButton,
            [data-testid="stMain"]:has(#admin-panel-page) .stElementContainer:has(.admin-back-target) + .stElementContainer .stButton > button {
                margin-left: auto !important;
            }

            .employee-manage-card {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 0.5rem;
            }

            .employee-manage-card h3 {
                margin: 0 0 0.25rem;
                font-size: 1.05rem;
            }

            .employee-manage-card p,
            .employee-progress-percent {
                margin: 0;
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.45;
            }

            .employee-progress-percent {
                white-space: nowrap;
                font-weight: 650;
            }

            .delete-course-panel,
            .leave-course-panel {
                border: 1px solid var(--line);
                border-radius: 16px;
                background: #ffffff;
                padding: 1rem;
                margin-bottom: 0.9rem;
            }

            .delete-course-panel h3,
            .leave-course-panel h3 {
                margin: 0 0 0.45rem;
                font-size: 1.05rem;
            }

            .delete-course-panel p,
            .leave-course-panel p {
                margin: 0.28rem 0;
                color: var(--muted);
                line-height: 1.5;
            }

            .delete-course-panel strong,
            .leave-course-panel strong {
                color: var(--text);
            }

            .employee-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                margin-bottom: 0.65rem;
                background: #ffffff;
            }

            .employee-row span {
                display: block;
                color: var(--muted);
                font-size: 0.92rem;
                margin-top: 0.15rem;
            }

            .stButton > button,
            .stFormSubmitButton > button {
                border-radius: 999px;
                border: 1px solid var(--line-strong);
                background: #f6f7f9 !important;
                color: var(--text) !important;
                min-height: 42px;
                font-weight: 650;
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
                box-shadow: none;
            }

            .stButton > button *,
            .stFormSubmitButton > button * {
                color: var(--text) !important;
                fill: var(--text) !important;
            }

            .stButton > button:hover,
            .stFormSubmitButton > button:hover {
                transform: translateY(-1px);
                background: #ffffff !important;
                border-color: #c7cbd3;
                color: var(--text) !important;
            }

            .stButton > button:focus,
            .stFormSubmitButton > button:focus {
                color: var(--text) !important;
                border-color: #bfc4cc;
                box-shadow: 0 0 0 3px rgba(210, 215, 224, 0.45);
            }

            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea {
                border-radius: 14px;
                border-color: var(--line-strong);
                background: #ffffff !important;
                color: var(--text) !important;
                -webkit-text-fill-color: var(--text) !important;
                caret-color: var(--text) !important;
                flex: 1 1 auto !important;
            }

            [data-testid="stTextInputRootElement"],
            [data-testid="stTextAreaRootElement"],
            div[data-baseweb="input"],
            div[data-baseweb="base-input"],
            div[data-baseweb="textarea"] {
                display: flex !important;
                align-items: center !important;
                position: relative !important;
                background: #ffffff !important;
                border-color: var(--line-strong) !important;
                border-radius: 14px !important;
                color: var(--text) !important;
                box-shadow: none !important;
            }

            [data-testid="stTextInputRootElement"] > div,
            [data-testid="stTextAreaRootElement"] > div,
            div[data-baseweb="input"] > div,
            div[data-baseweb="base-input"] > div,
            div[data-baseweb="textarea"] > div {
                background: #ffffff !important;
                color: var(--text) !important;
            }

            [data-testid="stTextInputRootElement"] div[data-baseweb="base-input"],
            div[data-baseweb="input"] div[data-baseweb="base-input"] {
                width: 100% !important;
                flex: 1 1 auto !important;
            }

            [data-testid="stTextInputRootElement"] div,
            div[data-baseweb="input"] div,
            div[data-baseweb="base-input"] div {
                background-color: #ffffff !important;
            }

            [data-testid="stTextInputRootElement"]:focus-within,
            div[data-baseweb="input"]:focus-within,
            div[data-baseweb="base-input"]:focus-within {
                border-color: #bfc4cc !important;
                box-shadow: 0 0 0 3px rgba(210, 215, 224, 0.45) !important;
            }

            [data-testid="stTextInput"] input::placeholder,
            [data-testid="stTextArea"] textarea::placeholder {
                color: #8a9099 !important;
                opacity: 1 !important;
            }

            [data-testid="stTextInputRootElement"] button,
            div[data-baseweb="input"] button,
            div[data-baseweb="base-input"] button,
            button[aria-label*="password" i],
            button[title*="password" i] {
                position: absolute !important;
                right: -12px !important;
                top: 50% !important;
                transform: translateY(-50%) !important;
                background: #ffffff !important;
                border: 0 !important;
                border-radius: 12px !important;
                color: #555b64 !important;
                min-height: 34px !important;
                box-shadow: none !important;
                margin-left: auto !important;
            }

            [data-testid="stTextInputRootElement"] button:hover,
            div[data-baseweb="input"] button:hover,
            div[data-baseweb="base-input"] button:hover,
            button[aria-label*="password" i]:hover,
            button[title*="password" i]:hover {
                background: #f3f4f6 !important;
                color: #333842 !important;
                transform: translateY(-50%) !important;
            }

            [data-testid="stTextInputRootElement"] svg,
            div[data-baseweb="input"] svg,
            div[data-baseweb="base-input"] svg,
            button[aria-label*="password" i] svg,
            button[title*="password" i] svg {
                color: #555b64 !important;
                fill: #555b64 !important;
            }

            [data-testid="stWidgetLabel"],
            [data-testid="stWidgetLabel"] label,
            [data-testid="stWidgetLabel"] p {
                color: var(--text) !important;
                opacity: 1 !important;
            }

            [data-testid="stRadio"],
            [data-testid="stRadio"] *,
            [role="radiogroup"],
            [role="radiogroup"] * {
                color: var(--text) !important;
                opacity: 1 !important;
            }

            [data-testid="stRadio"] {
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
            }

            [data-testid="stRadio"] [role="radiogroup"] {
                display: grid;
                gap: 0.38rem;
            }

            [data-testid="stRadio"] label,
            [role="radiogroup"] label {
                background: transparent !important;
            }

            [data-testid="stRadio"] p {
                color: var(--text) !important;
                font-size: 1rem !important;
                line-height: 1.45 !important;
            }

            [data-testid="stRadio"] label[data-baseweb="radio"] {
                display: flex !important;
                align-items: center !important;
                gap: 0.55rem !important;
                min-height: 28px !important;
                padding: 0.05rem 0 !important;
            }

            [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child,
            [role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
                width: 16px !important;
                height: 16px !important;
                min-width: 16px !important;
                min-height: 16px !important;
                flex: 0 0 16px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                border-radius: 50% !important;
                border: 2px solid #a4abb6 !important;
                background: #ffffff !important;
                box-shadow: none !important;
                margin: 0 !important;
            }

            [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child > div,
            [role="radiogroup"] label[data-baseweb="radio"] > div:first-child > div {
                width: 6px !important;
                height: 6px !important;
                min-width: 6px !important;
                min-height: 6px !important;
                border-radius: 50% !important;
                background: transparent !important;
                box-shadow: none !important;
                margin: 0 !important;
            }

            [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) > div:first-child,
            [role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) > div:first-child {
                border-color: var(--text) !important;
                background: #ffffff !important;
            }

            [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) > div:first-child > div,
            [role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) > div:first-child > div {
                background: var(--text) !important;
            }

            [data-testid="stRadio"] label[data-baseweb="radio"] > div:last-child,
            [role="radiogroup"] label[data-baseweb="radio"] > div:last-child {
                color: var(--text) !important;
                line-height: 1.45 !important;
            }

            [data-testid="stRadio"] input[type="radio"],
            [role="radiogroup"] input[type="radio"] {
                appearance: none !important;
                -webkit-appearance: none !important;
                width: 16px !important;
                height: 16px !important;
                min-width: 16px !important;
                min-height: 16px !important;
                border-radius: 50% !important;
                border: 2px solid #9aa3af !important;
                background: #ffffff !important;
                accent-color: var(--text) !important;
                margin: 0 0.45rem 0 0 !important;
            }

            [data-testid="stRadio"] input[type="radio"]:checked,
            [role="radiogroup"] input[type="radio"]:checked {
                border-color: var(--text) !important;
                background: radial-gradient(circle at center, var(--text) 0 38%, #ffffff 42% 100%) !important;
            }

            [data-testid="stRadio"] svg,
            [role="radiogroup"] svg {
                color: #9aa3af !important;
                fill: #ffffff !important;
                stroke: #9aa3af !important;
            }

            [data-testid="stRadio"] [aria-checked="true"] svg,
            [role="radiogroup"] [aria-checked="true"] svg {
                color: var(--text) !important;
                fill: var(--text) !important;
                stroke: var(--text) !important;
            }

            [data-testid="stProgress"] > div > div > div {
                background: #9aa3af;
            }

            [data-testid="stVerticalBlockBorderWrapper"] {
                border-color: var(--line);
                border-radius: 22px;
                background: var(--softer);
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:hover {
                border-color: var(--line-strong);
                transform: translateY(-2px);
                background: #ffffff;
            }

            .fade-in {
                animation: fadeIn 520ms ease both;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @media (max-width: 760px) {
                .topnav {
                    align-items: flex-start;
                    border-radius: 24px;
                    flex-direction: column;
                }

                .navlinks {
                    justify-content: flex-start;
                }

                .hero {
                    min-height: 460px;
                    padding-top: 2.5rem;
                }

                .template-grid {
                    grid-template-columns: 1fr;
                }

                .home-course-card-grid {
                    grid-template-columns: 1fr;
                }

                .sample-course-grid {
                    grid-template-columns: 1fr;
                }

                .sample-progress {
                    gap: 0;
                }

                .progress-circle {
                    width: 34px;
                    height: 34px;
                    flex-basis: 34px;
                    font-size: 0.9rem;
                }

                .contact-side {
                    position: static;
                }

                .employee-row {
                    align-items: flex-start;
                    flex-direction: column;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def public_nav(active_page: str) -> None:
    def active(name: str) -> str:
        return "active" if active_page == name else ""

    home_class = active("home")
    sample_class = active("sample_courses")
    contact_class = active("contact")

    st.markdown(
        f"""
        <nav class="topnav">
            <div class="brand">AI Skills Course Studio</div>
            <div class="navlinks">
                <a class="{home_class}" href="?page=home" target="_self">Home</a>
                <a class="{sample_class}" href="?page=sample_courses" target="_self">Sample Courses</a>
                <a href="?page=courses" target="_blank" rel="noopener noreferrer">Courses</a>
                <a class="{contact_class}" href="?page=contact" target="_self">Contact</a>
            </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )


def page_title(title: str, subtitle: str, centered: bool = False) -> None:
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    class_name = "section-title fade-in center-title" if centered else "section-title fade-in"
    st.markdown(
        f"""
        <div class="{class_name}">
            <h2>{title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
