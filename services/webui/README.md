[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://opensource.org/licenses/Apache-2.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/justmeloic/From-First-Principles/issues)
[![GitHub issues](https://img.shields.io/github/issues/justmeloic/From-First-Principles)](https://github.com/justmeloic/From-First-Principles/issues)
[![GitHub stars](https://img.shields.io/github/stars/justmeloic/From-First-Principles)](https://github.com/justmeloic/From-First-Principles/stargazers)

# From First Principles - Web UI Service

**Tags:** `web-ui` `frontend` `html` `css` `javascript` `website` `user-interface` `static-site`

This directory (`services/webui`) contains the source code for the web user interface of "From First Principles." This UI is responsible for presenting the website's content to users in a clear, accessible, and engaging manner.

**[Loïc Muhirwa](https://github.com/justmeloic/)**  initiated this project, and we enthusiastically welcome contributions from the community.

### Project Overview

The Web UI is built using standard web technologies: HTML, CSS, and JavaScript. It's designed to be lightweight and performant, providing a smooth user experience across different devices.

### Directory Structure

The `services/webui/src` directory is structured as follows:

*   **assets:** Contains static assets used by the website.
    *   **css:** Contains CSS stylesheets for styling the website.
        *   `animate.css`: A library for CSS animations.
        *   `bootstrap.min.css`: A CSS framework for responsive design.
        *   `font-awesome.min.css`: A library of icons.
        *   `magnific-popup.css`: A library for creating responsive lightboxes.
        *   `tooplate-style.css`: Custom styles for the website's theme (likely a template).
    *   **fonts:** Stores font files used on the website.
        *   `FontAwesome.otf`, `fontawesome-webfont.*`: Font Awesome font files in various formats.
    *   **images:** Contains images used on the website.
        *   `home-bg.jpg`: Background image for the homepage.
        *   `side.png`: Likely a sidebar or decorative image.
        *   `tab-logo.png`: The website's favicon or logo used in browser tabs.
    *   **js:** Contains JavaScript files for website functionality.
        *   `bootstrap.min.js`: The JavaScript component of the Bootstrap framework.
        *   `custom.js`: Custom JavaScript code for website-specific functionality.
        *   `jquery.js`: The jQuery library.
        *   `jquery.magnific-popup.min.js`: The JavaScript component of the Magnific Popup library.
        *   `jquery.parallax.js`: A library for creating parallax scrolling effects.
        *   `magnific-popup-options.js`: Configuration options for Magnific Popup.
        *   `render-article-text.js`: Likely responsible for dynamically rendering article content.
        *   `smoothscroll.js`: A library for smooth scrolling effects.
        *   `wow.min.js`: A library for triggering animations on scroll.
*   **content:** Contains the website's content, organized by category.
    *   **engineering:** Example content for the "Engineering" category.
        *   **post1:** Sample content for an engineering article.
            *   `blog-page.html`: An HTML template for displaying the blog post.
            *   `body.txt`: The text content of the blog post.
    *   **home:** Content for the website's homepage.
        *   **post1 & post2:** Sample content for homepage articles.
            *   `blog-page.html`: An HTML template for displaying the blog post.
            *   `body.md` & `body_simple.md`: The Markdown content of the blog post, possibly in different formats (full and simplified).
            *   `thumbnail.png`: A thumbnail image for the blog post.
*   **index.html:** The main HTML file for the website.
*   **pages:** Contains additional HTML pages for specific sections.
    *   `blog.html`: The blog page template.
    *   `engineering.html`: The engineering category page (optional).

### Development

#### Technologies Used

*   HTML5
*   CSS3 (with Bootstrap, Font Awesome, Animate.css, and Magnific Popup)
*   JavaScript (with jQuery)

#### Local Development

To run the website locally, you can simply open the `index.html` as the entry point for your dev server. 

#### Building

If you use `Live Server` there's nothing to build :) 

### Contributing

We encourage contributions to the Web UI! Please refer to the main project's `CONTRIBUTING_DEV.md` for guidelines on contributing code.

**Specific areas for contribution to the Web UI include:**

*   Improving the website's responsiveness and cross-browser compatibility.
*   Enhancing the user interface and user experience.
*   Adding new features or improving existing ones.
*   Optimizing performance.
*   Improving accessibility.
*   Updating or replacing outdated libraries.

**Join us in making "From First Principles" a beautiful and functional website!**