const navToggle = document.querySelector("[data-nav-toggle]");
const navMenu = document.querySelector("[data-nav-menu]");

if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
        const isOpen = navMenu.classList.toggle("open");
        navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    navMenu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            navMenu.classList.remove("open");
            navToggle.setAttribute("aria-expanded", "false");
        });
    });
}

const langDropdown = document.querySelector("[data-lang-dropdown]");
const langTrigger = document.querySelector("[data-lang-trigger]");
const langMenu = langDropdown ? langDropdown.querySelector(".lang-menu") : null;

if (langDropdown && langTrigger && langMenu) {
    const setOpen = (open) => {
        langMenu.classList.toggle("open", open);
        langTrigger.setAttribute("aria-expanded", String(open));
    };

    langTrigger.addEventListener("click", (event) => {
        event.stopPropagation();
        setOpen(!langMenu.classList.contains("open"));
    });

    document.addEventListener("click", (event) => {
        if (!langDropdown.contains(event.target)) {
            setOpen(false);
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            setOpen(false);
            langTrigger.blur();
        }
    });
}

const filterButtons = document.querySelectorAll("[data-filter]");
const menuCategories = document.querySelectorAll("[data-category]");

filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const filter = button.dataset.filter;

        filterButtons.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");

        menuCategories.forEach((category) => {
            category.hidden = filter !== "all" && category.dataset.category !== filter;
        });
    });
});

const messages = {
    named: document.body.dataset.alertNamed || "{name}",
    plain: document.body.dataset.alertPlain || "",
    tail: document.body.dataset.alertTail || "",
};

document.querySelectorAll("[data-demo-form]").forEach((form) => {
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);
        const name = String(formData.get("name") || "").trim();
        const greeting = name
            ? messages.named.replace("{name}", name)
            : messages.plain;

        window.alert(`${greeting} ${messages.tail}`.trim());
        form.reset();
    });
});

const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12 }
    );

    revealItems.forEach((item) => revealObserver.observe(item));
} else {
    revealItems.forEach((item) => item.classList.add("visible"));
}
