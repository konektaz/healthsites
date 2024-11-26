import type { Meta, StoryObj } from '@storybook/html';
// import { expect, userEvent, within } from '@storybook/test';

import { createPage } from './Page';

const meta = {
  title: 'Patterns/Page',
  render: () => createPage(),
  parameters: {
    layout: 'fullscreen',
  },
} satisfies Meta;

export default meta;

export const Default: StoryObj = {};
