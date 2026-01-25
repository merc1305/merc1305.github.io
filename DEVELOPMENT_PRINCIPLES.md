# Project Development Principles: Reliability & Anti-Regression

To ensure the stability and evolution of the **merc1305.github.io** project, every agent or developer MUST follow these principles:

## 1. Respect "Invisible" Features
The project contains many subtle optimizations (mobile paddings, specific margins, visited link colors).
- **Rule**: Never perform large-block replacements in HTML/CSS without first grepping for `@media`, `style=`, and `:visited`.
- **Action**: Use `multi_replace_file_content` with surgical precision rather than replacing entire sections.

## 2. Mandatory Mobile-First Verification
The project serves users on various devices, including mobile.
- **Rule**: Any change to `index.css` or HTML structure MUST be manually checked against mobile breakpoints (e.g., `< 768px`).
- **Checklist**:
    - [ ] Viewport meta tag is present.
    - [ ] No horizontal scrolling on mobile.
    - [ ] Tap targets are at least 44x44px.
    - [ ] Font sizes remain readable (min 16px/1rem for body).

## 3. Preservation of Information Hierarchy
The order of sections in `mining-stratum/index.html` is intentional.
- **Rule**: Relocating blocks (e.g., moving tutorials to the bottom) should only be done if explicitly requested.
- **Caution**: If refactoring, ensure that informational "help" blocks (tool-intro, tldr) are preserved and correctly styled.

## 4. History-Aware Development
- **Rule**: Before making a change, run `git diff HEAD~1` or check recent commit messages to understand what "features" were just added.
- **Goal**: Avoid reverting the previous agent's work.

## 5. Viewport Meta-Tag Persistence
- **Rule**: NEVER accidentally remove `<meta name="viewport" ...>` from HTML files. It is the single most critical line for mobile usability.

---
**Failure to follow these rules results in a broken user experience and technical debt.**
