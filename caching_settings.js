import { app } from "../../scripts/app.js";
import { api } from '../../scripts/api.js'

app.registerExtension({
	name: "caching.to.not.waste.settings",
	async setup() {
		caching_clear();
	},
	settings: [
		{
			id: "Caching to not Waste. When",
			name: "Clear cache",
			type: "combo",
			defaultValue: "never",
			options: [
				{ text: "Never", value: "never" },
				{ text: "Older Than", value: "older_than" }
			],
			attrs: {
				editable: true,
				filter: true,
			},
			onChange: (newVal, oldVal) => {
				caching_clear();
			},
		},
		{
			id: "Caching to not Waste.Days",
			name: "Days",
			type: "number",
			defaultValue: 365,
			attrs: {
				showButtons: true,
				maxFractionDigits: 3,
			},
			onChange: (newVal, oldVal) => {
				caching_clear();
			},
		}
	],
});

function caching_clear(){
	setTimeout(function() {
		console.log('When? ', app.extensionManager.setting.get('Caching to not Waste. When'));
		console.log('Days? ', app.extensionManager.setting.get('Caching to not Waste.Days'));

		if(app.extensionManager.setting.get('Caching to not Waste. When') != 'never'
			&& app.extensionManager.setting.get('Caching to not Waste.Days') > 0
		){
			send_message(app.extensionManager.setting.get('Caching to not Waste.Days'));
		}
	}, "1000");
}

function send_message(message) {
    const body = new FormData();
    body.append('message',message);
    api.fetchApi("/caching_clear", {
	  	method: "POST",
	  	body
	}).then(res => res.json())
  	.then(data => {
    	console.log("🟢 Caching to not Waste files deleted: ", data);
  	})
  	.catch(err => {
	    console.error("❌ Caching to not Waste error:", err);
 	});
}
