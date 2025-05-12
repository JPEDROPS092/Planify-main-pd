import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '2a1'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '7ce'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'ff2'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'd0b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', 'ea5'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '127'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '91d'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'bda'),
    routes: [
      {
        path: '/docs/backlog',
        component: ComponentCreator('/docs/backlog', 'ecc'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/getting-started/configuration',
        component: ComponentCreator('/docs/getting-started/configuration', 'b30'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/getting-started/installation',
        component: ComponentCreator('/docs/getting-started/installation', '490'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/getting-started/quick-start',
        component: ComponentCreator('/docs/getting-started/quick-start', 'c34'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/intro',
        component: ComponentCreator('/docs/intro', 'aed'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/authentication',
        component: ComponentCreator('/docs/user-guide/authentication', 'e37'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/dashboard',
        component: ComponentCreator('/docs/user-guide/dashboard', '369'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/calendar',
        component: ComponentCreator('/docs/user-guide/modules/calendar', '6ea'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/communications',
        component: ComponentCreator('/docs/user-guide/modules/communications', '5ea'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/costs',
        component: ComponentCreator('/docs/user-guide/modules/costs', 'dc0'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/documents',
        component: ComponentCreator('/docs/user-guide/modules/documents', 'd23'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/projects',
        component: ComponentCreator('/docs/user-guide/modules/projects', 'dc9'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/risks',
        component: ComponentCreator('/docs/user-guide/modules/risks', 'a79'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/tasks',
        component: ComponentCreator('/docs/user-guide/modules/tasks', 'd69'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/modules/teams',
        component: ComponentCreator('/docs/user-guide/modules/teams', 'a86'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/user-guide/overview',
        component: ComponentCreator('/docs/user-guide/overview', '01c'),
        exact: true,
        sidebar: "tutorialSidebar"
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '8d4'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
