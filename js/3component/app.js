class ReusableButton extends HTMLElement {
  constructor() {
    super();
    // 1. Attach a Shadow DOM for encapsulated styling
    this.attachShadow({ mode: 'open' });
  }

  // 2. Lifecycle callback: Runs when the element is added to the DOM
  connectedCallback() {
    this.render();
  }

  // 3. Define which attributes to watch for changes (like Figma properties)
  static get observedAttributes() {
    return ['variant'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      this.render();
    }
  }

  // 4. Render the component dynamically based on attributes
  render() {
    const variant = this.getAttribute('variant') || 'primary';

    this.shadowRoot.innerHTML = `
      <style>
        button {
          padding: 10px 20px;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-weight: bold;
          transition: background 0.2s ease;
        }
        .primary {
          background-color: #007acc;
          color: white;
        }
        .primary:hover {
          background-color: #005999;
        }
        .secondary {
          background-color: #e0e0e0;
          color: #333;
        }
        .secondary:hover {
          background-color: #cccccc;
        }
      </style>
      <button class="${variant}">
        <slot></slot> <!-- This displays whatever text is placed inside the tag -->
      </button>
    `;
  }
}

// 5. Register the custom element with the browser
customElements.define('my-button', ReusableButton);
