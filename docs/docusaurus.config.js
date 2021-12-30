// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Aviauth-API',
  tagline: 'Authorization service & Identity provider',
  url: 'https://docs.aviauth.com/',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.png',
  organizationName: 'julleks',
  projectName: 'aviauth-api',

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: 'latest',
          routeBasePath: 'latest',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/julleks/aviauth-api/tree/master/docs/',
        },
        blog: {
          path: 'changelog',
          routeBasePath: 'changelog',
          blogTitle: 'Changelog',
          blogSidebarTitle: 'Recent changes',
          showReadingTime: true,
          editUrl: 'https://github.com/julleks/aviauth-api/tree/master/docs/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Aviauth-API',
        logo: {
          alt: 'Aviauth Docs Logo',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Docs',
          },
          {to: '/changelog', label: 'Changelog', position: 'left'},
          {
            href: 'https://github.com/julleks/aviauth-api',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'aviauth-api',
                to: '/latest/intro',
              },
              {
                label: 'Swagger',
                to: 'https://api.aviauth.com/latest/docs/',
              },
              {
                label: 'ReDoc',
                to: 'https://api.aviauth.com/latest/redoc/',
              },
              {
                label: 'aviauth-microservice',
                href: 'https://microservice.aviauth.com',
              },
              {
                label: 'aviauth-fastapi',
                href: 'https://package.aviauth.com',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/aviauth',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/julleks/aviauth-api',
              },
              {
                label: 'Julleks',
                href: 'https://julleks.com',
              },
            ],
          },
        ],
        copyright: `© ${new Date().getFullYear()} Aviauth`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
