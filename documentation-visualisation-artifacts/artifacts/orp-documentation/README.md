# ORP Documentation

This is the repository for the single page of ORP API documentation that will be used in UAT.
It uses Nuxt.js and Tailwind.


## Commands
---

`npm i`

This will install the project dependencies.

`npm run dev`

This runs the development server which listens for file changes, and automatically builds/serves the updates.

### Generating static files
---

First, make sure the `router.base` in nuxt.config.json matches the folder structure of where the page will be hosted.
For instance, the project is currently deployed on `https://demo.bigmotive.com/orp/docs/`, so this value
is set to `/orp/docs`. This just makes sure that static assets can be resolved, otherwise CSS and JS might break.

Then run:

`npm run build`

This assembles the project into static files, which can be found in /dist.
After this, run:

`npm run generate`

This links the JS/CSS, and produces the final bundle of static files.

### Deploying
---


To deploy these static files, just drop the contents of `/dist` into any webserver.