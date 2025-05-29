import { app } from "../../scripts/app.js";

const TARGET_NODE_NAMES = new Set([
	// "caching_controlnet",
	// "Caching Controlnet Image to not Waste,
	"caching_image",
	"Caching Image to not Waste",

	"caching_mask",
	"Caching Mask to not Waste",

	"caching_text",
	"Caching Text to not Waste",

	"caching_condition",
	"Caching Conditioning to not Waste",

	"caching_from_combined_images",
	"Caching Combined Image to not Waste",
]);


app.registerExtension({
	name: "caching.to.not.waste.unique.name",
	async setup() {
		console.log("Caching to not waste unique name node, ready!")
	},
	async nodeCreated(node, app) {
		console.log(node)
		console.log(
			node?.title,
			!TARGET_NODE_NAMES.has(node?.title))

		if (!TARGET_NODE_NAMES.has(node?.title)) return;

		console.log("[identification watcher] node created:", node);

		const idWidget = node.widgets?.find(w => w.name === "identification");
		if (idWidget) {
			const oldCallback = idWidget.callback || (() => {});
			idWidget.callback = (val, widget, nodeInstance) => {
				oldCallback(val, widget, nodeInstance);
				ensureUniqueIdentification(nodeInstance);
			};
		}

		ensureUniqueIdentification(node);
	},
	loadedGraphNode(node, app) {
        if (!TARGET_NODE_NAMES.has(node?.title)) return;
        ensureUniqueIdentification(node);
    }
})

function ensureUniqueIdentification(targetNode) {
	const allNodes = app.graph._nodes;
	console.log('caralho => ', targetNode.title);
	const currentType = targetNode.title;

	const nodesOfSameType = allNodes.filter(n => n.title === currentType && n !== targetNode);

	nodesOfSameType.push(targetNode);

	const usedNames = new Set();

	for (const node of nodesOfSameType) {
		const idWidget = node.widgets?.find(w => w.name === "identification");
		if (!idWidget) continue;

		let baseId = idWidget.value || "id";
		let newId = baseId;
		let index = 0;

		while (usedNames.has(newId)) {
			newId = `${baseId}_${index++}`;
		}

		if (newId !== idWidget.value) {
			console.log(`[Caching Unique ID] Renaming duplicate ID "${idWidget.value}" to "${newId}"`);
			idWidget.value = newId;
			node.onWidgetChanged?.(idWidget, newId);
		}

		usedNames.add(idWidget.value);
	}
}


function getIdentificationValue(node) {
	const widget = node.widgets?.find(w => w.name === "identification");
	return widget?.value || null;
}