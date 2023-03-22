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
	    	if (details.hasOwnProperty('first_dose_dt') && details['first_dose_dt'] !== null) {
	    		let first_dose_field = document.getElementById(
	    				'id_vaccinesreceived_set-'+index+'-first_dose_dt');
	    		first_dose_field.value = details['first_dose_dt'];
	    		first_dose_field.readOnly = true;
	    		// Remove the calendar picker once readonly is set for the field.
	    		let first_calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-first_dose_dt .datetimeshortcuts');
	    		first_calendar_item.style.cssText = 'display:none';
	    	}
	    	// Second dose date
	    	if (details.hasOwnProperty('second_dose_dt') && details['second_dose_dt'] !== null) {
	    		console.log(details['second_dose_dt']);
	    		let second_dose_field = document.getElementById(
	    				'id_vaccinesreceived_set-'+index+'-second_dose_dt');
	    		second_dose_field.value = details['second_dose_dt'];
	    		second_dose_field.readOnly = true;
	    		// Remove the calendar picker once readonly is set for the field.
	    		let second_calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-second_dose_dt .datetimeshortcuts');
	    		second_calendar_item.style.cssText = 'display:none';
	    	} 
	    	// Third dose date
	    	if (details.hasOwnProperty('third_dose_dt') && details['third_dose_dt'] !== null) {
	    		let third_dose_field = document.getElementById(
	    				'id_vaccinesreceived_set-'+index+'-third_dose_dt');
	    		third_dose_field.value = details['third_dose_dt'];
	    		third_dose_field.readOnly = true;
	    		// Remove the calendar picker once readonly is set for the field.
	    		let third_calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-third_dose_dt .datetimeshortcuts');
	    		third_calendar_item.style.cssText = 'display:none';
	    	}
	    }

	    function resetRelatedFields(index) {
	    	// First dose date
    		let first_dose_field = document.getElementById(
    				'id_vaccinesreceived_set-'+index+'-first_dose_dt');
    		first_dose_field.value = '';
    		first_dose_field.readOnly = false;
    		// Reset for the calendar picker.
    		let first_calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-first_dose_dt .datetimeshortcuts');
    		first_calendar_item.style.cssText = 'display:inline-block';

    		// Second dose date
    		let second_dose_field = document.getElementById(
    				'id_vaccinesreceived_set-'+index+'-second_dose_dt');
    		second_dose_field.value = '';
    		second_dose_field.readOnly = false;
    		// Reset for the calendar picker.
    		let second_calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-second_dose_dt .datetimeshortcuts');
    		second_calendar_item.style.cssText = 'display:inline-block';

    		// Third dose date
    		let third_dose_field = document.getElementById(
    				'id_vaccinesreceived_set-'+index+'-third_dose_dt');
    		third_dose_field.value = '';
    		third_dose_field.readOnly = false;
    		// Reset for the calendar picker.
    		let third_calendar_item = document.querySelector('#vaccinesreceived_set-'+index+' .field-third_dose_dt .datetimeshortcuts');
    		third_calendar_item.style.cssText = 'display:inline-block';
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