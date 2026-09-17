/**
 * Interactive SVG Generator and Exporter
 * Creates a synchronized interactive group with an encapsulated stylesheet.
 */
class InteractiveSVGApp {
  // SVG Configuration Constraints
  static SVG_NS = "http://w3.org";
  static VIEWBOX = { width: 300, height: 200 };
  
  constructor(containerId, exportBtnId) {
    this.container = document.getElementById(containerId);
    this.exportBtn = document.getElementById(exportBtnId);
    
    this.svgElement = null;
    this.groupElement = null;

    this.init();
  }

  /**
   * Initializes components and binds interaction event hooks
   */
  init() {
    this.buildSVGContext();
    this.bindEvents();
  }

  /**
   * Assembles the vector node tree structural layers
   */
  buildSVGContext() {
    const { width, height } = InteractiveSVGApp.VIEWBOX;

    // 1. Root Canvas
    this.svgElement = document.createElementNS(InteractiveSVGApp.SVG_NS, "svg");
    this.svgElement.setAttribute("width", width.toString());
    this.svgElement.setAttribute("height", height.toString());
    this.svgElement.setAttribute("viewBox", `0 0 ${width} ${height}`);

    // 2. Interactive Compound Wrapper (<g>)
    this.groupElement = document.createElementNS(InteractiveSVGApp.SVG_NS, "g");
    this.groupElement.setAttribute("class", "interactive-group");

    // 3. Background Primitive Bounding Shape
    const rect = document.createElementNS(InteractiveSVGApp.SVG_NS, "rect");
    rect.setAttribute("x", "50");
    rect.setAttribute("y", "25");
    rect.setAttribute("width", "200");
    rect.setAttribute("height", "150");
    rect.setAttribute("fill", "#3498db");
    rect.setAttribute("opacity", "0.8"); // 80% explicit base transparency
    rect.setAttribute("rx", "10");

    // 4. Central Graphic Character Unit
    const text = document.createElementNS(InteractiveSVGApp.SVG_NS, "text");
    text.setAttribute("x", "150");
    text.setAttribute("y", "115");
    text.setAttribute("fill", "#ffffff");
    text.setAttribute("font-size", "70");
    text.setAttribute("font-weight", "bold");
    text.setAttribute("text-anchor", "middle");
    text.textContent = "A";

    // Structural Composition
    this.groupElement.appendChild(rect);
    this.groupElement.appendChild(text);
    this.svgElement.appendChild(this.groupElement);
    
    // Inject node tree directly into target UI element
    this.container.appendChild(this.svgElement);
  }

  /**
   * Attaches action handlers to UI triggers
   */
  bindEvents() {
    this.exportBtn.addEventListener("click", () => this.handleExport());
  }

  /**
   * Encapsulates the animation styling payload for standalone files
   * @returns {SVGStyleElement}
   */
  generateEmbeddedStyles() {
    const styleElement = document.createElementNS(InteractiveSVGApp.SVG_NS, "style");
    styleElement.textContent = `
      .interactive-group {
        cursor: pointer;
        transform-origin: 150px 100px;
        transition: opacity 0.2s ease;
      }
      @keyframes pulseGroup {
        0% { transform: scale(1); }
        50% { transform: scale(1.15); }
        100% { transform: scale(1); }
      }
      .interactive-group:hover {
        animation: pulseGroup 0.5s ease-in-out forwards;
      }
      .interactive-group:active {
        opacity: 0.7;
      }
    `;
    return styleElement;
  }

  /**
   * Handles XML Serialization process and triggers browser download pipeline
   */
  handleExport() {
    const styles = this.generateEmbeddedStyles();
    
    // Injects structural styles safely before processing string mapping
    this.svgElement.insertBefore(styles, this.svgElement.firstChild);

    // Serialization Pipeline execution
    const serializer = new XMLSerializer();
    let xmlSource = serializer.serializeToString(this.svgElement);

    // Dynamic clean up ensures active runtime remains uncluttered
    this.svgElement.removeChild(styles);

    // Validate standard SVG namespaces
    if (!xmlSource.includes('xmlns="http://w3.org"')) {
      xmlSource = xmlSource.replace(/^<svg/, `<svg xmlns="${InteractiveSVGApp.SVG_NS}"`);
    }
    
    const formattedPayload = `<?xml version="1.0" encoding="utf-8"?>\n${xmlSource}`;
    
    this.triggerDownload(formattedPayload, "synchronized-interactive-rect.svg");
  }

  /**
   * Triggers file download window automatically via standard Blob injection
   * @param {string} dataPayload - Raw XML structural content payload string
   * @param {string} fileName - Destination asset identity
   */
  triggerDownload(dataPayload, fileName) {
    const url = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(dataPayload)}`;
    
    const downloadAnchor = document.createElement("a");
    downloadAnchor.href = url;
    downloadAnchor.download = fileName;
    
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    document.body.removeChild(downloadAnchor);
  }
}

// Instantiate the application layer safely on DOM Load
document.addEventListener("DOMContentLoaded", () => {
  new InteractiveSVGApp("canvas-container", "export-btn");
});
