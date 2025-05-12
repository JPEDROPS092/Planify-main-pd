/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introdução',
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Primeiros Passos',
      items: [
        'getting-started/installation',
        'getting-started/configuration',
        'getting-started/quick-start',
      ],
    },
    {
      type: 'category',
      label: 'Guia do Usuário',
      items: [
        'user-guide/overview',
        'user-guide/authentication',
        'user-guide/dashboard',
        {
          type: 'category',
          label: 'Módulos',
          items: [
            'user-guide/modules/projects',
            'user-guide/modules/tasks',
            'user-guide/modules/teams',
            'user-guide/modules/risks',
            'user-guide/modules/costs',
            'user-guide/modules/documents',
            'user-guide/modules/communications',
            'user-guide/modules/calendar',
          ],
        },
      ],
    },
    // Backlog do Projeto
    {
      type: 'doc',
      label: 'Backlog do Projeto',
      id: 'backlog',
    },
    // Commented out sections that don't have corresponding files yet
    /*
    {
      type: 'category',
      label: 'Guia do Desenvolvedor',
      items: [
        'developer-guide/architecture',
        'developer-guide/backend',
        'developer-guide/frontend',
        'developer-guide/api-reference',
        'developer-guide/contributing',
      ],
    },
    {
      type: 'category',
      label: 'Administração',
      items: [
        'admin/deployment',
        'admin/security',
        'admin/backup',
        'admin/monitoring',
      ],
    },
    {
      type: 'category',
      label: 'FAQ',
      items: ['faq/general', 'faq/technical'],
    },
    */
  ],
};

module.exports = sidebars;
