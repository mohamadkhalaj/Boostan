Telegram.WebApp.MainButton.showProgress(true);
Telegram.WebApp.ready();
const initData = Telegram.WebApp.initData || "";
const initDataUnsafe = Telegram.WebApp.initDataUnsafe || {};
var origin = window.location.origin + '/';

if (!Telegram.WebApp.isExpanded) {
  Telegram.WebApp.expand();
}

function getElement(id) {
	return document.getElementById(id);
}

getElement('login_btn').addEventListener('click', login_button_clicked);
getElement('submit-btn-web').addEventListener('click', submit);
getElement('main-menu-close').addEventListener('click', close_main_menu);
getElement('session-menu-close').addEventListener('click', close_session_menu);
getElement('forgot-code').addEventListener('click', get_forget_code);
getElement('sessions').addEventListener('click', open_session_menu);
getElement('contribute').addEventListener('click', open_contribute_menu);
getElement('user-name').addEventListener('click', main_menu);
getElement('contribute-menu-close').addEventListener('click', close_contribute_menu);
getElement('close-alert').addEventListener('click', close_alert);

var indexes = [];
var session_lists = [];
var food_list;
var reserve_list = {'total':0, 'days':[]};
var created_objects = [];
var food_list_response_status;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const cancel_text = tags['cancel'];
const reserve_text = tags['reserve'];
const already_reserved_text = tags['already_reserved'];
const not_reserved_text = tags['not_reserved'];
const logout_text = tags['logout'];
const insufficient_balance_text = tags['insufficient_balance'];
const meal_submit_text = tags['meal_submit'];
const telegram_main_btn_order_text = tags['telegram_main_btn_order'];
const sending_data_loading_text = tags['sending_data_loading'];
const telegram_main_btn_sending_data_loading_text = tags['telegram_main_btn_sending_data_loading'];
const breakfast_text = tags['breakfast'];
const lunch_text = tags['lunch'];
const order_button_text = tags['order_button'];
const dinner_text = tags['dinner'];
const login_text_message = tags['login'];
const reserve_food_text_message = tags['reserve_food'];
const get_food_list_text_message = tags['food_list'];
const success_food_list_text_message = tags['success_food_list'];
const get_forget_code_text_message = tags['forget_code'];
const sessions_ip_text = tags['sessions_ip'];
const sessions_os_text = tags['sessions_os'];
const sessions_browser_text = tags['sessions_browser'];
const sessions_last_used_text = tags['sessions_last_used'];
const sessions_device_text = tags['sessions_device'];
const sessions_current_device_text = tags['sessions_current_device'];

const passwordInput = document.querySelector("[type='password']");
const togglePasswordButton = getElement("toggle-password");
togglePasswordButton.addEventListener("click", togglePassword);
function togglePassword() {
	if (passwordInput.type === "password") {
	  passwordInput.type = "text";
	} else {
	  passwordInput.type = "password";
	}
}

Telegram.WebApp.MainButton.hideProgress();
Telegram.WebApp.MainButton.setText(telegram_main_btn_order_text).onClick(submit);
Telegram.WebApp.BackButton.show().onClick(Telegram.WebApp.close);

const login_form = getElement('login-form');
const student_password = getElement('student_password');
const student_number = getElement('student_number');
const login_btn = getElement("login_btn");
const forgotten_code_btn = getElement('forgot-code-btn');
const submit_btn = getElement('submit-btn-web-text');

student_number.addEventListener("keypress", function(event) {
	if (event.key === "Enter" && login_form.style.display === "block") {
	  event.preventDefault();
	  student_password.focus();
	}
  });

student_password.addEventListener("keypress", function(event) {
	if (event.key === "Enter" && login_form.style.display === "block") {
	  event.preventDefault();
	  login_btn.click();
	  login_btn.focus();
	}
  });

function create_days(){
	let parent_day_cards = getElement('day-cards');
	food_list['days'].forEach(function(item, index) {

		// create elements
		let day_card_div = document.createElement('div');
		let day_card_title = document.createElement('h5');
		let day_card_body = document.createElement('div');
		let day_card_row = document.createElement('div');
		let day_card_breakfast = document.createElement('div');
		let day_card_lunch = document.createElement('div');
		let day_card_dinner = document.createElement('div');
		let day_card_breakfast_meal = document.createElement('div');
		let day_card_lunch_meal = document.createElement('div');
		let day_card_dinner_meal = document.createElement('div');		
		let day_card_breakfast_self = document.createElement('p');
		let day_card_lunch_self = document.createElement('p');
		let day_card_dinner_self = document.createElement('p');
		let day_card_breakfast_img = document.createElement('img');
		let day_card_lunch_img = document.createElement('img');
		let day_card_dinner_img = document.createElement('img');
		let day_card_breakfast_overlay = document.createElement('div');
		let day_card_lunch_overlay = document.createElement('div');
		let day_card_dinner_overlay = document.createElement('div');
		let day_card_breakfast_overlay_text = document.createElement('div');
		let day_card_lunch_overlay_text = document.createElement('div');
		let day_card_dinner_overlay_text = document.createElement('div');	
		let day_card_breakfast_status = document.createElement('p');
		let day_card_lunch_status = document.createElement('p');
		let day_card_dinner_status = document.createElement('p');

		// assign classes
		day_card_div.className = 'card shadow-card mt-3'
		day_card_title.className = "card-header text-sm-center"
		day_card_body.className = 'card-body'
		day_card_row.className = 'row text-center'

		day_card_breakfast.className = 'col-4'
		day_card_lunch.className = 'col-4'
		day_card_dinner.className = 'col-4'

		// meal
		day_card_breakfast_meal.className = 'meal'
		day_card_lunch_meal.className = 'meal'
		day_card_dinner_meal.className = 'meal'

		day_card_breakfast_self.className = 'self-text'
		day_card_lunch_self.className = 'self-text'
		day_card_dinner_self.className = 'self-text'

		let breakfast_status = true;
		let lunch_status = true;
		let dinner_status = true;
		let breakfast_reservation_status = false;
		let lunch_reservation_status = false;
		let dinner_reservation_status = false;
		if (item['breakfast'].length == 0 ) {
			day_card_breakfast_img.className = 'meal-avatar disabled-image'
			breakfast_status = false;
		}
		else {
			day_card_breakfast_img.className = 'meal-avatar'
		}
		if (item['lunch'].length == 0 ) {
			day_card_lunch_img.className = 'meal-avatar disabled-image'
			lunch_status = false;
		}
		else {
			day_card_lunch_img.className = 'meal-avatar'
		}
		if (item['dinner'].length == 0 ) {
			day_card_dinner_img.className = 'meal-avatar disabled-image'
			dinner_status = false;
		}
		else {
			day_card_dinner_img.className = 'meal-avatar'
		}

		day_card_breakfast_overlay.className = 'overlay'
		day_card_lunch_overlay.className = 'overlay'
		day_card_dinner_overlay.className = 'overlay'

		day_card_breakfast_overlay_text.className = 'text'
		day_card_lunch_overlay_text.className = 'text'
		day_card_dinner_overlay_text.className = 'text'

		breakfast_reservation_status = meal_reservation_status(item['breakfast'], 'breakfast')
		lunch_reservation_status = meal_reservation_status(item['lunch'], 'lunch')
		dinner_reservation_status = meal_reservation_status(item['dinner'], 'dinner')
		

		if (breakfast_reservation_status[0]) {
			day_card_breakfast_status.className = 'btn meal-caption d-block bg-success'
		}
		else {
			day_card_breakfast_status.className = 'btn meal-caption d-block bg-danger'
		}
		if (lunch_reservation_status[0]) {
			day_card_lunch_status.className = 'btn meal-caption d-block bg-success'
		}
		else {
			day_card_lunch_status.className = 'btn meal-caption d-block bg-danger'
		}
		if (dinner_reservation_status[0]) {
			day_card_dinner_status.className = 'btn meal-caption d-block bg-success'
		}
		else {
			day_card_dinner_status.className = 'btn meal-caption d-block bg-danger'
		}
		
		// get day data
		day_name = item['day']
		day_date = item['date']
		day_index = item['index']

		if (!indexes.includes(day_index)) {
			indexes.push(day_index)
		}

		// assign id
		day_card_div.id = "day_" + day_index
		day_card_breakfast_meal.id = "day_br_" + day_index
		day_card_lunch_meal.id = "day_lu_" + day_index
		day_card_dinner_meal.id = "day_di_" + day_index

		// assign day title value
		day_card_title.innerText = day_name + ' ' + day_date

		// assign images src and alt
		day_card_breakfast_img.src = '/static/images/breakfast.png'
		day_card_breakfast_img.alt = 'breakfast'
		day_card_lunch_img.src = '/static/images/lunch.png'
		day_card_lunch_img.alt = 'lunch'
		day_card_dinner_img.src = '/static/images/dinner.png'
		day_card_dinner_img.alt = 'dinner'

		// assign overlay text
		day_card_breakfast_overlay_text.innerText = breakfast_text
		day_card_lunch_overlay_text.innerText = lunch_text
		day_card_dinner_overlay_text.innerText = dinner_text

		// assign self
		if (breakfast_reservation_status[0]) {
			day_card_breakfast_self.innerText = breakfast_reservation_status[0]
			day_card_breakfast_status.innerText = already_reserved_text
		}
		else {
			day_card_breakfast_self.innerText = get_default_self(item['breakfast'])[0]
			day_card_breakfast_status.innerText  = not_reserved_text
		}
		if (lunch_reservation_status[0]) {
			day_card_lunch_self.innerText = lunch_reservation_status[0]
			day_card_lunch_status.innerText= already_reserved_text
		}
		else {
			day_card_lunch_self.innerText = get_default_self(item['lunch'])[0]
			day_card_lunch_status.innerText = not_reserved_text
		}
		if (dinner_reservation_status[0]) {
			day_card_dinner_self.innerText = dinner_reservation_status[0]
			day_card_dinner_status.innerText= already_reserved_text
		}
		else {
			day_card_dinner_self.innerText = get_default_self(item['dinner'])[0]
			day_card_dinner_status.innerText = not_reserved_text
		}

		// check status class


		// append childs

		// overlay -> overlay text
		day_card_breakfast_overlay.appendChild(day_card_breakfast_overlay_text)
		day_card_lunch_overlay.appendChild(day_card_lunch_overlay_text)
		day_card_dinner_overlay.appendChild(day_card_dinner_overlay_text)

		// meal -> self, image, overlay, status
		if (breakfast_status) {
			day_card_breakfast_meal.appendChild(day_card_breakfast_self)
			day_card_breakfast_meal.addEventListener('click', meal_clicked)
		}
		if (lunch_status){
			day_card_lunch_meal.appendChild(day_card_lunch_self)
			day_card_lunch_meal.addEventListener('click', meal_clicked)
		}
		if (dinner_status){
			day_card_dinner_meal.appendChild(day_card_dinner_self)
			day_card_dinner_meal.addEventListener('click', meal_clicked)
		}

		day_card_breakfast_meal.appendChild(day_card_breakfast_img)
		day_card_lunch_meal.appendChild(day_card_lunch_img)
		day_card_dinner_meal.appendChild(day_card_dinner_img)


		if (breakfast_status) {
			day_card_breakfast_meal.appendChild(day_card_breakfast_overlay)
		}
		if (lunch_status){
			day_card_lunch_meal.appendChild(day_card_lunch_overlay)
		}
		if (dinner_status){
			day_card_dinner_meal.appendChild(day_card_dinner_overlay)
		}

		if (breakfast_status) {
			day_card_breakfast_meal.appendChild(day_card_breakfast_status)
		}
		if (lunch_status){
			day_card_lunch_meal.appendChild(day_card_lunch_status)
		}
		if (dinner_status){
			day_card_dinner_meal.appendChild(day_card_dinner_status)
		}

		// day -> meal
		day_card_breakfast.appendChild(day_card_breakfast_meal)
		day_card_lunch.appendChild(day_card_lunch_meal)
		day_card_dinner.appendChild(day_card_dinner_meal)

		// row -> day
		day_card_row.appendChild(day_card_breakfast)
		day_card_row.appendChild(day_card_lunch)
		day_card_row.appendChild(day_card_dinner)

		// card body -> row
		day_card_body.appendChild(day_card_row)

		// card -> title, body
		day_card_div.appendChild(day_card_title)
		day_card_div.appendChild(day_card_body)

		// parent -> others
		parent_day_cards.appendChild(day_card_div)
		created_objects.push(day_card_div)

		create_meal_menu(item['breakfast'], breakfast_text, breakfast_reservation_status[1], breakfast_reservation_status[2], day_card_breakfast_meal.id, item['day'], item['date'], item['index'])
		create_meal_menu(item['lunch'], lunch_text, lunch_reservation_status[1], lunch_reservation_status[2], day_card_lunch_meal.id, item['day'], item['date'], item['index'])
		create_meal_menu(item['dinner'], dinner_text, dinner_reservation_status[1], dinner_reservation_status[2], day_card_dinner_meal.id, item['day'], item['date'], item['index'])
	})
}


function create_meal_menu(meal, meal_name, self_id, food_id, meal_id, day, date, index){
	if (meal.length > 0) {
			let body = document.getElementsByTagName('body')[0];
			let navbar = document.getElementsByClassName('navbar')[0];

			let meal_menu = document.createElement('div');
			let meal_menu_title = document.createElement('div');
			let meal_menu_title_row = document.createElement('div');
			let meal_menu_title_name = document.createElement('div');
			let meal_menu_title_day = document.createElement('div');
			let meal_menu_title_date = document.createElement('div');

			meal_menu.id = 'meal_menu_' + meal_id

			meal_menu.className = 'meal-menu p-2 text-sm-center'
			meal_menu_title.className = 'alert fixed-top text-center submit-btn'
			meal_menu_title_row.className = 'row'
			meal_menu_title_name.className = 'col-4'
			meal_menu_title_day.className = 'col-4'
			meal_menu_title_date.className = 'col-4'

			meal_menu_title_name.innerText = meal_name
			meal_menu_title_day.innerText = day
			meal_menu_title_date.innerText = date

			meal_menu_title_row.appendChild(meal_menu_title_name);
			meal_menu_title_row.appendChild(meal_menu_title_day);
			meal_menu_title_row.appendChild(meal_menu_title_date);

			meal_menu_title.appendChild(meal_menu_title_row);
			meal_menu.appendChild(meal_menu_title);

			let meal_menu_body = document.createElement('div');
			let meal_menu_body_row = document.createElement('div');

			meal_menu_body.className = 'container'
			meal_menu_body_row.className = 'row'

			meal.forEach(function(item, index) {
				if (item['price'] != null) {
					if (meal.length == 2) {
						let meal_menu_body_col1_left_edge = document.createElement('div');
						let meal_menu_body_col1_right_edge = document.createElement('div');
						let meal_menu_body_col1 = document.createElement('div');

						meal_menu_body_col1_left_edge.className = 'col-2'
						meal_menu_body_col1_right_edge.className = 'col-2'
						meal_menu_body_col1.className = 'col-8'

						let meal_menu_body_col1_food_item = document.createElement('div');
						let meal_menu_body_col1_card = document.createElement('div');
						let meal_menu_body_col1_card_div = document.createElement('div');
						let meal_menu_body_col1_card_text = document.createElement('h5');
						let meal_menu_body_col1_card_text_price = document.createElement('p');

						meal_menu_body_col1_food_item.className = 'card food-items'
						meal_menu_body_col1_card.className = 'card-body p-4'
						meal_menu_body_col1_card_div.className = 'text-center'
						meal_menu_body_col1_card_text.className = 'fw-bolder'

						meal_menu_body_col1_card_text.innerText = item['name']
						meal_menu_body_col1_card_text.setAttribute('value', item['value'])
						meal_menu_body_col1_card_text.setAttribute('index', index)
						meal_menu_body_col1_card_text_price.innerText = pretty_numbers(item['price']) + ' تومان'
						meal_menu_body_col1_card_text_price.setAttribute('value', item['price'])

						let meal_menu_body_col1_card_btn = document.createElement('div');
						let meal_menu_body_col1_card_btn_inner = document.createElement('div');
						let meal_menu_body_col1_card_btn_inner_a = document.createElement('a');

						meal_menu_body_col1_card_btn.className = "card-footer p-4 pt-0 border-top-0 bg-transparent"
						meal_menu_body_col1_card_btn_inner.className = 'text-center'
						meal_menu_body_col1_card_btn_inner_a.className = 'btn btn-danger mt-auto'

					   if (item['value'] == food_id) {
							meal_menu_body_col1_card_btn_inner_a.innerText = cancel_text
						}
						else {
							 meal_menu_body_col1_card_btn_inner_a.innerText = reserve_text   
							 meal_menu_body_col1_card_btn_inner_a.className = 'btn btn-success mt-auto res-btn'
						}

						meal_menu_body_col1_card_btn_inner_a.addEventListener('click', cancel_reserve_btn)

						meal_menu_body_col1_card_btn_inner.appendChild(meal_menu_body_col1_card_btn_inner_a);
						meal_menu_body_col1_card_btn.appendChild(meal_menu_body_col1_card_btn_inner);

						meal_menu_body_col1_card_div.appendChild(meal_menu_body_col1_card_text);
						meal_menu_body_col1_card_div.appendChild(meal_menu_body_col1_card_text_price);
						meal_menu_body_col1_card.appendChild(meal_menu_body_col1_card_div);

						meal_menu_body_col1_food_item.appendChild(meal_menu_body_col1_card);
						meal_menu_body_col1_food_item.appendChild(meal_menu_body_col1_card_btn);
						meal_menu_body_col1.appendChild(meal_menu_body_col1_food_item);

						meal_menu_body_row.appendChild(meal_menu_body_col1_left_edge);
						meal_menu_body_row.appendChild(meal_menu_body_col1);
						meal_menu_body_row.appendChild(meal_menu_body_col1_right_edge);
					}
					else if (meal.length == 3) {
						let meal_menu_body_col1 = document.createElement('div');

						meal_menu_body_col1.className = 'col-6'

						let meal_menu_body_col1_food_item = document.createElement('div');
						let meal_menu_body_col1_card = document.createElement('div');
						let meal_menu_body_col1_card_div = document.createElement('div');
						let meal_menu_body_col1_card_text = document.createElement('h5');
						let meal_menu_body_col1_card_text_price = document.createElement('p');

						meal_menu_body_col1_food_item.className = 'card food-items'
						meal_menu_body_col1_card.className = 'card-body p-4'
						meal_menu_body_col1_card_div.className = 'text-center'
						meal_menu_body_col1_card_text.className = 'fw-bolder'

						meal_menu_body_col1_card_text.innerText = item['name']
						meal_menu_body_col1_card_text_price.innerText = pretty_numbers(item['price']) + ' تومان'
						meal_menu_body_col1_card_text_price.setAttribute('value', item['price'])

						let meal_menu_body_col1_card_btn = document.createElement('div');
						let meal_menu_body_col1_card_btn_inner = document.createElement('div');
						let meal_menu_body_col1_card_btn_inner_a = document.createElement('a');

						meal_menu_body_col1_card_btn_inner_a.addEventListener('click', cancel_reserve_btn)

						meal_menu_body_col1_card_btn.className = "card-footer p-4 pt-0 border-top-0 bg-transparent"
						meal_menu_body_col1_card_btn_inner.className = 'text-center'
						meal_menu_body_col1_card_btn_inner_a.className = 'btn btn-danger mt-auto'

						if (item['value'] == food_id) {
							meal_menu_body_col1_card_btn_inner_a.innerText = cancel_text
						}
						else {
							 meal_menu_body_col1_card_btn_inner_a.innerText = reserve_text   
							 meal_menu_body_col1_card_btn_inner_a.className = 'btn btn-success mt-auto res-btn'
						}

						meal_menu_body_col1_card_btn_inner.appendChild(meal_menu_body_col1_card_btn_inner_a);
						meal_menu_body_col1_card_btn.appendChild(meal_menu_body_col1_card_btn_inner);

						meal_menu_body_col1_card_div.appendChild(meal_menu_body_col1_card_text);
						meal_menu_body_col1_card_div.appendChild(meal_menu_body_col1_card_text_price);
						meal_menu_body_col1_card.appendChild(meal_menu_body_col1_card_div);

						meal_menu_body_col1_food_item.appendChild(meal_menu_body_col1_card);
						meal_menu_body_col1_food_item.appendChild(meal_menu_body_col1_card_btn);
						meal_menu_body_col1.appendChild(meal_menu_body_col1_food_item);

						meal_menu_body_row.appendChild(meal_menu_body_col1);
					}
				}
			})
			
			meal_menu_body.appendChild(meal_menu_body_row);
			let form = document.createElement('form')
			form.id = 'self-form'
			let self_select = document.createElement('select');
			self_select.setAttribute('onChange', 'change_self(this)')
			self_select.className = 'custom-select mt-3 alert alert-danger self'
			let has_selected = false;
			let options_ar = []
			meal[0]['self'].forEach(function(inner_item, index) {
				let option = document.createElement('option');
				option.innerText = inner_item['name'];
				option.value = inner_item['value'];
				if (inner_item['value'] == self_id) {
					option.setAttribute('selected', '');
					has_selected = true
				}
				options_ar.push(option)
				self_select.appendChild(option);
			})
			if (!has_selected) {
				options_ar.forEach(function(s_item, index) {
					if (get_default_self(meal)[1] == s_item.value) {
						s_item.setAttribute('selected', '');
					}
				})
			}
			options_ar = []
			form.appendChild(self_select);
			meal_menu_body.appendChild(form);
			let alert = document.createElement('div');
			alert.className = 'alert-balance alert alert-warning';
			alert.innerText = insufficient_balance_text;
			let submit = document.createElement('button');
			submit.className = 'btn btn-primary w-100 submit-btn';
			submit.innerText = meal_submit_text;
			submit.addEventListener('click', submit_meal_menu)
			meal_menu_body.appendChild(alert);
			meal_menu_body.appendChild(submit);
			meal_menu.appendChild(meal_menu_body);
			body.insertBefore(meal_menu, navbar)
			created_objects.push(meal_menu);
	}
}

function pretty_numbers(number) {
	number = parseFloat(number).toFixed(1)/10;
	return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

function meal_reservation_status(day, meal) {
	let found = [false, false, false];
	day.forEach(function(item, index) {
		if (item['selected'] == true && item['price'] != null) {
			found[2] = item['value']
			item['self'].forEach(function(self_item, self_index) {
				if(self_item['selected'] == true) {
					found[0] = self_item['name']
					found[1] = self_item['value']
				}
			})
		}
	})
	if (found[0]) {
		found[0] = clean_self_name(found[0]);
	}
	return found;
}

function get_default_self(meal) {
	let found = [false, false];
	meal.forEach(function(item, index) {
		item['self'].forEach(function(self, index) {
			if (!found[0]) {
				found[0] = self['name']
				found[1] = self['value']
			}
			if (self['default'] == true) {
				found[0] = self['name']
				found[1] = self['value']
			}
		})
	})
	if (found[0]) {
		found[0] = clean_self_name(found[0]);
	}
	return found;
}

function clean_self_name(self) {
	self = self.replace('خوابگاه', 'خ');
	self = self.replace('شهيد', '');
	self = self.replace('سلف', '');
	return self;
}

function submit_meal_menu() {
	if (parseFloat($('#user-credit').attr('value')) >= 0) {
		let parent = getElement(this.parentElement.parentElement.id.replace('meal_menu_', ''))
		let self;
		this.parentElement.childNodes[1].childNodes[0].childNodes.forEach(function(item, index){
			if (item.hasAttribute('selected')){
				self = item.innerText
			}
		})
		self = clean_self_name(self);
		parent.childNodes[0].innerText = self;

		if (this.parentElement.childNodes[0].innerText.includes(cancel_text)) {
			parent.childNodes[3].innerText = already_reserved_text;
			parent.childNodes[3].className = 'btn meal-caption d-block bg-success';
		}
		else {
			parent.childNodes[3].innerText = not_reserved_text;
			parent.childNodes[3].className = 'btn meal-caption d-block bg-danger';
		}
		this.parentElement.parentElement.classList.remove('meal-menu-visible');
		document.getElementsByClassName('meal-menu-wrapper')[0].classList.remove('meal-menu-wrapper-show');
		show_order_btn()
	}
	else {
		// better alert
		$(".alert-balance").show();
	}
}

function meal_clicked() {
	$(".alert-balance").hide();
	let menu_id = "meal_menu_" + this.id;
	getElement(menu_id).classList.add('meal-menu-visible');
	document.getElementsByClassName('meal-menu-wrapper')[0].classList.add('meal-menu-wrapper-show');
	if (check_user_supports_haptic_or_no()) {
		Telegram.WebApp.HapticFeedback.selectionChanged();
	}
	hide_order_btn();
}

function check_uniq_reserve(node) {
	let node_parent = node.parentNode.parentNode.parentNode.parentNode;
	let childs = node_parent.parentNode.childNodes;
	let price = 0;
	if (childs.length == 2) {
		childs.forEach(function(item, index){

			if (item.className != 'col-2' && item.parentNode.parentNode !== node_parent) {
				var child_obj = item.childNodes[0].childNodes[1].childNodes[0].childNodes[0];
				if (child_obj.innerText == cancel_text) {

					price = parseFloat(item.childNodes[0].childNodes[0].childNodes[0].childNodes[1].getAttribute('value'))
					child_obj.innerText = reserve_text
					child_obj.className = 'btn btn-success mt-auto res-btn'
					child_obj.addEventListener('click', cancel_reserve_btn)
				}
			}
		})
	}
	return price;
}

function get_food_price(node) {
	return parseFloat(node.parentNode.parentNode.parentNode.childNodes[0].childNodes[0].childNodes[1].getAttribute('value'));
}

function change_self(this_obj) {
	var strUser = this_obj.options[this_obj.selectedIndex];
	console.log(strUser);
	this_obj.childNodes.forEach(function(item, index) {
		item.removeAttribute('selected')
	})
	strUser.setAttribute('selected', '')
}

function cancel_reserve_btn() {
	if (check_user_supports_haptic_or_no()) {
		Telegram.WebApp.HapticFeedback.selectionChanged();
	}
	let price = get_food_price(this)
	let credit = parseFloat($('#user-credit').attr('value'))
	if (this.innerText == reserve_text) {
		let others_price = check_uniq_reserve(this);
		this.innerText = cancel_text
		this.className = 'btn btn-danger mt-auto res-btn'
		credit = credit - price + others_price
	}
	else {
		this.innerText = reserve_text   
		this.className = 'btn btn-success mt-auto res-btn'
		credit = credit + price
	}
	$('#user-credit').text("اعتبار: " + pretty_numbers(credit) + " تومان");
	$('#user-credit').attr('value', credit);
}


function submit() {
	submit_btn.disabled = true;
	reserve_list = {'total':0, 'days':[]}
	meals = ['br', 'lu', 'di']
	indexes.forEach(function(item, index){
		meals.forEach(function(meal, index){
			let id = `meal_menu_day_${meal}_${item}`
			let menu = getElement(id);
			if (menu != null) {
				menu.childNodes[1].childNodes[0].childNodes.forEach(function(food_item, index) {
					if (food_item.className != 'col-2' && food_item.childNodes[0].innerHTML.includes(cancel_text)){
						let base = food_item.childNodes[0].childNodes[0].childNodes[0];
						let price = parseFloat(base.childNodes[1].getAttribute('value'));
						let food = parseFloat(base.childNodes[0].getAttribute('value'));

						let self_select = menu.childNodes[1].childNodes[1].childNodes[0].childNodes
						let self;
						self_select.forEach(function(s_item, index) {
							if(s_item.hasAttribute('selected')) {
								self = s_item.value
							}
						})
						create_submit_list(food, price, self, meal, item)
					}
				})
			}
		})
	})
	// send request

	sending_data_loading();
	var xhr = new XMLHttpRequest();
	xhr.open("POST", `${origin}api/v1/reserve-food/`, true);
	let session = localStorage.getItem('session');
	params = `csrfmiddlewaretoken=${csrftoken}&session=${session}&food-list=` + JSON.stringify(reserve_list)
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	xhr.onreadystatechange = function() { // Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE) {

			if (this.status === 200) {
				let message = JSON.parse(xhr.responseText)['message']
				create_alert_notification(message, 'success')
				if (check_user_supports_haptic_or_no()) {
					Telegram.WebApp.HapticFeedback.notificationOccurred('success');
				}
			}
			else {
				let message = JSON.parse(xhr.responseText)
				// check relogin attr  
				if (message['relogin']) {
					show_login_page();
				}
				create_alert_notification(message['error'], 'danger')
				if (check_user_supports_haptic_or_no()) {
					Telegram.WebApp.HapticFeedback.notificationOccurred('error');
				}
			}
			submit_btn.disabled = false;
			reset_order_btn_text();
		}
	};
	create_alert_notification(reserve_food_text_message, 'warning')
	xhr.send(params);
	// Telegram.WebApp.close()
}

function create_alert_notification(message, type) {
	getElement('alert-container').style.visibility = 'visible';
	let alert_obj = getElement('success-alert');
	let tel_type = type == 'danger' ? 'error' : type;
	if (check_user_supports_haptic_or_no()){
		Telegram.WebApp.HapticFeedback.notificationOccurred(tel_type);
	}
	if (!alert_obj) {
		let parent_alert = document.getElementsByClassName('container alert-message')[0];
		let alert_main = document.createElement('div');
		alert_main.id = 'success-alert';
		alert_main.className = 'alert alert-success';

		let alert_button = document.createElement('button');
		alert_button.className = 'close';
		alert_button.innerText = 'x'
		alert_button.setAttribute('type', 'button');
		alert_button.setAttribute('data-dismiss', 'alert');

		let alert_text = document.createElement('p');
		alert_text.id = 'request-alert-message';

		alert_main.appendChild(alert_button);
		alert_main.appendChild(alert_text);
		parent_alert.appendChild(alert_main);

		alert_obj = alert_main;
	}

	alert_obj.style.display = 'block'
	alert_obj.className = 'alert alert-' + type
	$('#request-alert-message').text(message);

	// setTimeout(function(param){
	//     alert_obj.style.display = 'none'
	// }.bind(null), 5000000);
}

function create_submit_list(food, price, self, meal, item) {

	let meal_reserve = {
		'name': meal,
		'self': parseInt(self),
		'food': parseInt(food),
	}

	let exists = [false, false];
	reserve_list['days'].forEach(function(l_item, l_index) {
		if (l_item['index'] == item) {
			exists[0] = true;
			exists[1] = l_index;
		}
	})
	if (exists[0]) {
		reserve_list['days'][exists[1]]['meals'].push(meal_reserve)
	}
	else {
		let day_reserve = {
			'index': item,
			'meals': []
		}

		day_reserve['meals'].push(meal_reserve)
		reserve_list['days'].push(day_reserve)
	}
	reserve_list['total'] += price
}

function login_and_place_list(){
	hide_order_btn();
	let session = localStorage.getItem('session');
	var xhr = new XMLHttpRequest();
	xhr.open("POST", `${origin}api/v1/get-food-list/`, true);
	params = `csrfmiddlewaretoken=${csrftoken}&session=${session}`
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	xhr.onreadystatechange = function() { // Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE) {
			food_list_response_status = this.status;
			if (this.status === 200) {
				let message = JSON.parse(xhr.responseText)['food_list']
				create_alert_notification(success_food_list_text_message, 'success');
				food_list = message;
				document.getElementsByClassName('navbar-container')[0].style.visibility='visible';
				$('#user-name').text(food_list['name']);
				$('#user-credit').text("اعتبار: " + pretty_numbers(food_list['credit']) + " تومان");
				$('#user-credit').attr('value', food_list['credit'])
				show_order_btn();
				Telegram.WebApp.MainButton.enable();
				create_days()
				if (!Object.keys(initDataUnsafe).length) {
					getElement('submit-btn-web').style.display = 'block';
				}
			}
			else {
				let message = JSON.parse(xhr.responseText)
				// check relogin attr  
				if (message['relogin']) {
					show_login_page();
				}
				if (Object.keys(message).includes('student')) {
					document.getElementsByClassName('navbar-container')[0].style.visibility='visible';
					$('#user-name').text(message['student']['name']);
					$('#user-credit').text("اعتبار: " + pretty_numbers(message['student']['credit']) + " تومان");
					$('#user-credit').attr('value', message['student']['credit'])
				}
				create_alert_notification(message['error'], 'danger')
			}
		}
	};
	create_alert_notification(get_food_list_text_message, 'warning');
	xhr.send(params);
}

function check_login() {
	// get session from local storage
	let session = localStorage.getItem('session');
	if (session == null) {
		// login
		show_login_page();
	}
	else {
		// get food list
		login_and_place_list()
	}
}

function login_button_clicked() {
	get_session_from_api(student_number.value, student_password.value);
}

function remove_objects(){
	document.getElementsByClassName('navbar-container')[0].style.visibility='hidden';
	created_objects.forEach(function(item, index){
		var child = item.lastElementChild; 
		while (child) {
			item.removeChild(child);
			child = item.lastElementChild
		}
		item.remove()
	})
}

function get_session_from_api(username, password) {
	login_btn.disabled = true;
	let telegram_data = {
		'id': "",
		'username': "",
	}
	if (Object.keys(initDataUnsafe).length != 0){
		telegram_data['id'] = initDataUnsafe.user.id;
		telegram_data['username'] = initDataUnsafe.user.username;
	}
	var xhr = new XMLHttpRequest();
	xhr.open("POST", `${origin}api/v1/login/`, true);
	params = `csrfmiddlewaretoken=${csrftoken}&stun=${username}&password=${password}&telegram_data=${JSON.stringify(telegram_data)}`
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function() { // Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE) {

			if (this.status === 200) {
				let response = JSON.parse(xhr.responseText)
				let session = response['session']
				localStorage.setItem('session', session)
				let message = response['message']
				getElement('login-form').style.visibility='hidden'
				getElement('login-form').style.display='none'
				create_alert_notification(message, 'success')
				login_and_place_list()
			}
			else {
				let message = JSON.parse(xhr.responseText)
				if (message['relogin']) {
					show_login_page();
				}
				create_alert_notification(message['error'], 'danger')
			}
			login_btn.disabled = false;
		}
	};
	create_alert_notification(login_text_message, 'warning')
	xhr.send(params);
}

function main_menu() {
	hide_order_btn();
	if (check_user_supports_haptic_or_no()) {
		Telegram.WebApp.HapticFeedback.selectionChanged();
	}
	document.getElementsByClassName('meal-menu-wrapper')[0].classList.add('meal-menu-wrapper-show')
	getElement('main-menu').style.visibility = "visible";
}

function close_main_menu(){
	getElement('main-menu').style.visibility = "hidden";
	document.getElementsByClassName('meal-menu-wrapper')[0].classList.remove('meal-menu-wrapper-show')
	show_order_btn();
}

function close_session_menu(){
	getElement('session-menu').style.visibility = "hidden";
	getElement('main-menu').style.visibility = "visible";
}

function get_forget_code() {
	forgotten_code_btn.disabled = true;
	var xhr = new XMLHttpRequest();
	xhr.open("POST", `${origin}api/v1/get-forget-code/`, true);
	let session = localStorage.getItem('session');
	params = `csrfmiddlewaretoken=${csrftoken}&session=${session}`
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function() { // Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE) {

			if (this.status === 200) {
				let response = JSON.parse(xhr.responseText)['message'];
				create_alert_notification(response, 'success');
			}
			else {
				let message = JSON.parse(xhr.responseText)
				if (message['relogin']) {
					show_login_page();
				}
				create_alert_notification(message['error'], 'danger')
			}
			forgotten_code_btn.disabled = false;
		}
	};
	create_alert_notification(get_forget_code_text_message, 'warning')
	xhr.send(params);
}

function create_sessions(sessions) {
	let session = localStorage.getItem('session');
	let parent = getElement('session-menu-parent');
	sessions.forEach(function (item, index) {
		let useragent = item['user_agent'];

		let session_container = document.createElement('div');
		session_container.className = 'container session-cards';

		let session_text = document.createElement('div');
		session_text.className = 'session-text'

		let session_Browser = document.createElement('div');
		session_Browser.className = 'session-items';
		session_Browser.innerText = sessions_browser_text + useragent['browser'] + ` ${useragent['browser-version']}`;
		let session_OS = document.createElement('div');
		session_OS.className = 'session-items';
		session_OS.innerText = sessions_os_text + useragent['os'] + ` ${useragent['os-version']}`;
		let session_Device = document.createElement('div');
		session_Device.className = 'session-items';
		session_Device.innerText = sessions_device_text +  useragent['device'];
		let session_IP = document.createElement('div');
		session_IP.className = 'session-items';
		session_IP.innerText = sessions_ip_text + item['ip_address'];
		let session_LAST_USED = document.createElement('div');
		session_LAST_USED.className = 'session-items';
		session_LAST_USED.innerText = sessions_last_used_text + item['last_used'];
		if (item['session'] == session) {
			session_LAST_USED.innerText += sessions_current_device_text;
		}

		let session_logout_btn = document.createElement('button');
		session_logout_btn.className = 'btn submit-btn w-100';
		session_logout_btn.innerText = logout_text;
		session_logout_btn.id = item['session'];
		session_logout_btn.addEventListener('click', logout);

		session_text.appendChild(session_Browser);
		session_text.appendChild(session_OS);
		session_text.appendChild(session_Device);
		session_text.appendChild(session_IP);
		session_text.appendChild(session_LAST_USED);

		session_container.appendChild(session_text);
		session_container.appendChild(session_logout_btn);

		parent.appendChild(session_container);
		session_lists.push(session_container);
	})
}


function logout() {
	let main_this = this;
	var xhr = new XMLHttpRequest();
	xhr.open("POST", `${origin}api/v1/logout/`, true);
	let main_session = localStorage.getItem('session');
	let session = this.id;
	params = `csrfmiddlewaretoken=${csrftoken}&session=${session}`
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function() { // Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE) {

			if (this.status === 200) {
				let response = JSON.parse(xhr.responseText)
				create_alert_notification(response['message'], 'success')
				main_this.parentNode.remove();
				if (main_session == session) {
					close_session_menu();
					close_contribute_menu();
					close_main_menu();
					show_login_page();
				}
			}
			else {
				let message = JSON.parse(xhr.responseText)
				create_alert_notification(message['error'], 'danger')
			}
		}
	};
	xhr.send(params);
}

function rempve_sessions() {
	session_lists.forEach(function(item, index){
		var child = item.lastElementChild; 
		while (child) {
			item.removeChild(child);
			child = item.lastElementChild
		}
		item.remove()
	})
}

function get_sessions() {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", `${origin}api/v1/get-sessions/`, true);
	let session = localStorage.getItem('session');
	params = `csrfmiddlewaretoken=${csrftoken}&session=${session}`
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function() { // Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE) {

			if (this.status === 200) {
				let response = JSON.parse(xhr.responseText)
				rempve_sessions();
				create_sessions(response['message']);
			}
			else {
				let message = JSON.parse(xhr.responseText)
				create_alert_notification(message['error'], 'danger')
			}
		}
	};
	xhr.send(params);
}

function show_login_page(){
	hide_order_btn();
	forgotten_code_btn.disabled = false;
	login_btn.disabled = false;
	submit_btn.disabled = false;
	getElement('login-form').style.visibility='visible'
	getElement('login-form').style.display='block'
	student_number.focus();
	getElement('submit-btn-web').style.display = 'none';
	remove_objects()
	localStorage.removeItem('session');
}

function open_session_menu() {
	getElement('main-menu').style.visibility = "hidden";
	getElement('session-menu').style.visibility = "visible";
	get_sessions()
}

function open_contribute_menu(){
	getElement('main-menu').style.visibility = "hidden";
	getElement('contribute-menu').style.visibility = "visible";
}

function close_contribute_menu(){
	getElement('contribute-menu').style.visibility = "hidden";
	getElement('main-menu').style.visibility = "visible";
}

function close_alert() {
	getElement('alert-container').style.visibility = 'hidden';
}

function sending_data_loading() {
	Telegram.WebApp.MainButton.showProgress(true);
	Telegram.WebApp.MainButton.setText(telegram_main_btn_sending_data_loading_text);
	Telegram.WebApp.MainButton.disable();

	if (!Object.keys(initDataUnsafe).length) {
		getElement('submit-btn-web-text').innerText = sending_data_loading_text;
	}
}

function reset_order_btn_text() {
	Telegram.WebApp.MainButton.setText(telegram_main_btn_order_text);
	if (!Object.keys(initDataUnsafe).length) {
		getElement('submit-btn-web-text').innerText = order_button_text;
	}
	Telegram.WebApp.MainButton.hideProgress();
}

function hide_order_btn() {
	if (!Object.keys(initDataUnsafe).length) {
		getElement('submit-btn-web').style.display = 'none';
	}
	Telegram.WebApp.MainButton.hide();
}

function show_order_btn() {
	if (food_list_response_status == 200) {
		if (!Object.keys(initDataUnsafe).length) {
			getElement('submit-btn-web').style.display = 'block';
		}
		Telegram.WebApp.MainButton.show();
	}
}

function check_user_supports_haptic_or_no(){
	let tg_version = parseFloat(Telegram.WebApp.version);
	let tg_data_available = Object.keys(initDataUnsafe).length;
	return tg_data_available && tg_version >= 6.1;
}

Telegram.WebApp.MainButton.disable();
check_login()