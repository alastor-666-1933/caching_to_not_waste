import { app } from "../../scripts/app.js";

app.registerExtension({
	name: "caching.to.not.waste.coloring",
	async setup() {
		console.log("Caching to not waste coloring node, ready!")
	},
	async nodeCreated(node, app) {
		console.log(node)
	    const customNodes = [
	      "Caching Controlnet Image to not Waste",
	      "Caching Image to not Waste",
	      "Caching Mask to not Waste",
	      "Caching Text to not Waste",
	      "Caching Conditioning to not Waste",
	      "Caching Combined Image to not Waste",
	    ];

	    if (customNodes.includes(node?.title)) {
	      const rgb     = "rgb(204, 134, 0)";
	      node.color    = rgb;
	      node.bgcolor  = "rgba(204, 134, 0, 0.1)";
	      node.boxcolor = rgb;
	    }

	    console.log("[ColorNodes] Node estilizado:", node.title);
	    // delete ext.nodeCreated;
	  }
})