import { createHeader } from './Header';

export const createPage = () => {
  const article = document.createElement('article');
  let header: HTMLElement | null = null;

  const createHeaderElement = () => {
    return createHeader();
  };

  header = createHeaderElement();
  article.appendChild(header);

  const section = `
  <div>Section</div>
`;

  article.insertAdjacentHTML('beforeend', section);

  return article;
};
