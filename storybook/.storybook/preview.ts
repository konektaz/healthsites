import type { Preview } from "@storybook/html";

export const parameters = {
  backgrounds: {
    disable: true,
  },
};

export const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};
