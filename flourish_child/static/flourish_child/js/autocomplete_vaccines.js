/**
 * VACCINES RECEIVED AUTOCOMPLETE DATES JS:
 * Add listener for Vaccines inlines, monitor vaccine selected from choice options
 * get selected vaccine and query previous object for dose dates already completed
 * finally populate the dose dates against vaccine on the form
 * **/
$(document).ready(function () {
	(function($) {
		var form_id = 'id_vaccinesreceived_set-TOTAL_FORMS';
		var total_formset = document.getElementById(form_id).textContent;
		var error_message = '';
	
		if (total_formset && total_formset > 0) {
			for (count = 0; count < total_formset; count++) {
				addListener(count);
			}
		}
	
	    $(document).on('formset:added', function(event, $row, formsetName) {
	    	let form_count = document.getElementById(form_id).value - 1;
	        addListener(form_count);
	    });
			
	    function addListener(index) {
	    	let select_id = 'id_vaccinesreceived_set-'+index+'-received_vaccine_name';
			let select_field = document.getElementById(select_id);
			$(document).on('change', '#'+select_id, function() {
				// Reset values already completed before querying for related dates.
				resetRelatedFields(index);

				setLoading(true);
				selected = select_field.value;
				console.log(selected);
				// Query from previous model instances for date(s) completed (if any).
				if (selected) {
					updateDates(selected, index);
				} else {
					setLoading(false);
				}
			});
	    }
	    
	    async function updateDates(selected = '', index=0) {
	    	let url = '/flourish_child/received_dates/' + selected + '/';
	    	try {
	    		let response = await fetch(url);
	        	if (response.status === 200) {
	        		let data = await response.json();
	        		if (Object.keys(data).length > 0) {
	        			// Update corresponding date fields.
		        		updateRelatedFields(index, data);
	        		}
	        		
	        		// Toggle error message and loading (remove).
	        		toggleErrorMessage(error_message, index);
	        		setLoading(false);
	        		return;
	        	}

	        	// Toggle error message and loading (add and display to user).
	        	toggleErrorMessage('Failed to auto-fill dates for selected vaccine.', index);
	        	setLoading(false);

	    	} catch (err) {
	    		setLoading(false);
	    		console.error(err);
	    	}
	    }
	    
	    function setLoading(loading=false) {
	    	let loader = document.getElementById('loader');
	    	if (loading) {
	    		loader.classList.remove('hide-loader');
	    	} else {
	    		loader.classList.add('hide-loader');
	    	}
	    	
	    }

	    function updateRelatedFields(index, details) {
	    	// First dose date
	    	prefill('first_dose_dt', details, index);
	    	
	    	// Second dose date
	    	prefill('second_dose_dt', details, index);

	    	// Third dose date
	    	prefill('third_dose_dt', details, index);

	    	// Booster dose date
	    	prefill('booster_dose_dt', details, index);
	    	
	    	// 2nd Booster dose date
	    	prefill('booster_2nd_dose_dt', details, index);
	    	
	    	// 3rd Booster dose date
	    	prefill('booster_3rd_dose_dt', details, index);
	    }

	    function prefill(field, data, index) {
	    	if (data.hasOwnProperty(field) && data[field] !== null) {
	    		let dose_field = document.getElementById('id_vaccinesreceived_set-'+index+'-'+field);
	    		dose_field.value = data[field];
	    		dose_field.readOnly = true;
	    		// Remove the calendar picker once readonly is set for the field.
	    		let calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-'+field+' .datetimeshortcuts');
	    		calendar_item.style.cssText = 'display:none';
	    	}
	    }

	    function resetRelatedFields(index) {
	    	// First dose date
	    	clearfill('first_dose_dt', index);

    		// Second dose date
	    	clearfill('second_dose_dt', index);

    		// Third dose date
	    	clearfill('third_dose_dt', index);

	    	// Booster dose date
	    	clearfill('booster_dose_dt', index);
	    	
	    	// 2nd Booster dose date
	    	clearfill('booster_2nd_dose_dt', index);
	    	
	    	// 3rd Booster dose date
	    	clearfill('booster_3rd_dose_dt', index);
	    }
	    
	    function clearfill(field, index) {
	    	let dose_field = document.getElementById('id_vaccinesreceived_set-'+index+'-'+field);
	    	dose_field.value = '';
	    	dose_field.readOnly = false;
	    	// Reset for the calendar picker.
    		let calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-'+field+' .datetimeshortcuts');
    		calendar_item.style.cssText = 'display:inline-block';
	    	
	    }
	    
	    function toggleErrorMessage(message='', index) {

	    	// If no error message, remove if already existing.
	    	let field_class = document.getElementsByClassName('field-received_vaccine_name')[index];
	    	field_class.classList.remove('errors');
    		let errorlist_elem = document.getElementsByClassName('errorlist')[0];

    		if (errorlist_elem) {
    			field_class.removeChild(errorlist_elem);
    		}
	    	
	    	if (message) {
	    		// Add a 'ul' element for the error list, and append message.
	    		field_class.classList.add('errors');
	    	    
		    	let errorlist_elem = document.createElement("ul");
		    	errorlist_elem.classList.add('errorlist');
		    	
		    	let error_node = document.createElement("li");
		    	let error_text = document.createTextNode(message);

		    	error_node.appendChild(error_text);

		    	errorlist_elem.appendChild(error_node);
		    	field_class.appendChild(errorlist_elem);
	    	}
	    }
	
	})(django.jQuery);
});