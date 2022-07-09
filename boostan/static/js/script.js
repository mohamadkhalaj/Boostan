Telegram.WebApp.MainButton.showProgress(true);
Telegram.WebApp.ready();
const initData = Telegram.WebApp.initData || "";
const initDataUnsafe = Telegram.WebApp.initDataUnsafe || {};
var origin = window.location.origin + '/';

if (!Telegram.WebApp.isExpanded) {
  Telegram.WebApp.expand();
}

document.getElementById('login_btn').addEventListener('click', login_button_clicked);
document.getElementById('submit-btn-web').addEventListener('click', submit);

Telegram.WebApp.MainButton.hideProgress();
Telegram.WebApp.MainButton.setText('Order').show().onClick(submit);
Telegram.WebApp.BackButton.show().onClick(Telegram.WebApp.close);

var indexes = [];
var food_list;
var reserve_list = {'total':0, 'days':[]}
var created_objects = []

function create_days(){
	let parent_day_cards = document.getElementById('day-cards');
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
		day_card_breakfast_overlay_text.innerText = 'صبحانه'
		day_card_lunch_overlay_text.innerText = 'نهار'
		day_card_dinner_overlay_text.innerText = 'شام'

		// assign self
		if (breakfast_reservation_status[0]) {
			day_card_breakfast_self.innerText = breakfast_reservation_status[0]
			day_card_breakfast_status.innerText = 'رزرو شده'
		}
		else {
			day_card_breakfast_self.innerText = get_default_self(item['breakfast'])[0]
			day_card_breakfast_status.innerText  = 'رزرو نشده'
		}
		if (lunch_reservation_status[0]) {
			day_card_lunch_self.innerText = lunch_reservation_status[0]
			day_card_lunch_status.innerText= 'رزرو شده'
		}
		else {
			day_card_lunch_self.innerText = get_default_self(item['lunch'])[0]
			day_card_lunch_status.innerText = 'رزرو نشده'
		}
		if (dinner_reservation_status[0]) {
			day_card_dinner_self.innerText = dinner_reservation_status[0]
			day_card_dinner_status.innerText= 'رزرو شده'
		}
		else {
			day_card_dinner_self.innerText = get_default_self(item['dinner'])[0]
			day_card_dinner_status.innerText = 'رزرو نشده'
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

        create_meal_menu(item['breakfast'], 'صبحانه', breakfast_reservation_status[1], breakfast_reservation_status[2], day_card_breakfast_meal.id, item['day'], item['date'], item['index'])
        create_meal_menu(item['lunch'], 'نهار', lunch_reservation_status[1], lunch_reservation_status[2], day_card_lunch_meal.id, item['day'], item['date'], item['index'])
        create_meal_menu(item['dinner'], 'شام', dinner_reservation_status[1], dinner_reservation_status[2], day_card_dinner_meal.id, item['day'], item['date'], item['index'])
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
                            meal_menu_body_col1_card_btn_inner_a.innerText = 'کنسل'
                        }
                        else {
                             meal_menu_body_col1_card_btn_inner_a.innerText = 'رزرو'   
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
                            meal_menu_body_col1_card_btn_inner_a.innerText = 'کنسل'
                        }
                        else {
                             meal_menu_body_col1_card_btn_inner_a.innerText = 'رزرو'   
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
            alert.innerText = 'موجودی کافی نیست!'
            let submit = document.createElement('button');
            submit.className = 'btn btn-primary w-100 submit-btn';
            submit.innerText = 'اعمال تغییرات'
            submit.addEventListener('click', submit_meal_menu)
            meal_menu_body.appendChild(alert);
            meal_menu_body.appendChild(submit);
            meal_menu.appendChild(meal_menu_body);
            body.insertBefore(meal_menu, navbar)
            created_objects.push(meal_menu)
    }
}

function pretty_numbers(number) {
    number = parseFloat(number).toFixed(1)/10;
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "٫");
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
        found[0] = found[0].replace('خوابگاه', 'خ');
        found[0] = found[0].replace('شهيد', '');
        found[0]= found[0].replace('سلف', '');
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

        found[0] = found[0].replace('خوابگاه', 'خ');
        found[0] = found[0].replace('شهيد', '');
        found[0] = found[0].replace('سلف', '');
    }
    return found;
}

function submit_meal_menu() {
    if (parseFloat($('#user-credit').attr('value')) >= 0) {
        let parent = document.getElementById(this.parentElement.parentElement.id.replace('meal_menu_', ''))
        let self;
        this.parentElement.childNodes[1].childNodes[0].childNodes.forEach(function(item, index){
            if (item.hasAttribute('selected')){
                self = item.innerText
            }
        })
        self = self.replace('خوابگاه', 'خ');
        self = self.replace('شهيد', '');
        self = self.replace('سلف', '');
        parent.childNodes[0].innerText = self;

        if (this.parentElement.childNodes[0].innerText.includes('کنسل')) {
            parent.childNodes[3].innerText = 'رزرو شده'
            parent.childNodes[3].className = 'btn meal-caption d-block bg-success'
        }
        else {
            parent.childNodes[3].innerText = 'رزرو نشده'
            parent.childNodes[3].className = 'btn meal-caption d-block bg-danger'
        }
        this.parentElement.parentElement.classList.remove('meal-menu-visible')
        document.getElementsByClassName('meal-menu-wrapper')[0].classList.remove('meal-menu-wrapper-show')
        Telegram.WebApp.MainButton.setText('Order')
        Telegram.WebApp.MainButton.enable()
    }
    else {
        // better alert
        $(".alert-balance").show()
    }
}

function meal_clicked() {
    $(".alert-balance").hide()
    let menu_id = "meal_menu_" + this.id
    document.getElementById(menu_id).classList.add('meal-menu-visible')
    document.getElementsByClassName('meal-menu-wrapper')[0].classList.add('meal-menu-wrapper-show')
    Telegram.WebApp.MainButton.disable()
    Telegram.WebApp.MainButton.setText('Order')
}

function check_uniq_reserve(node) {
    let node_parent = node.parentNode.parentNode.parentNode.parentNode;
    let childs = node_parent.parentNode.childNodes;
    let price = 0;
    if (childs.length == 2) {
        childs.forEach(function(item, index){

            if (item.className != 'col-2' && item.parentNode.parentNode !== node_parent) {
                var child_obj = item.childNodes[0].childNodes[1].childNodes[0].childNodes[0];
                if (child_obj.innerText == 'کنسل') {

                    price = parseFloat(item.childNodes[0].childNodes[0].childNodes[0].childNodes[1].getAttribute('value'))
                    child_obj.innerText = 'رزرو'
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
    let price = get_food_price(this)
    let credit = parseFloat($('#user-credit').attr('value'))
    if (this.innerText == 'رزرو') {
        let others_price = check_uniq_reserve(this);
        this.innerText = 'کنسل'
        this.className = 'btn btn-danger mt-auto res-btn'
        credit = credit - price + others_price
    }
    else {
        this.innerText = 'رزرو'   
        this.className = 'btn btn-success mt-auto res-btn'
        credit = credit + price
    }
    $('#user-credit').text("اعتبار: " + pretty_numbers(credit) + " تومان");
    $('#user-credit').attr('value', credit);
}


function submit() {
    reserve_list = {'total':0, 'days':[]}
    meals = ['br', 'lu', 'di']
    indexes.forEach(function(item, index){
        meals.forEach(function(meal, index){
            let id = `meal_menu_day_${meal}_${item}`
            let menu = document.getElementById(id);
            if (menu != null) {
                menu.childNodes[1].childNodes[0].childNodes.forEach(function(food_item, index) {
                    if (food_item.className != 'col-2' && food_item.childNodes[0].innerHTML.includes('کنسل')){
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

    Telegram.WebApp.MainButton.showProgress(true);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", `${origin}api/v1/reserve-food/`, true);
    let session = localStorage.getItem('session');
    params = `session=${session}&food-list=` + JSON.stringify(reserve_list)
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE) {

            if (this.status === 200) {
                let message = JSON.parse(xhr.responseText)['message']
                create_notif(message, 'success')
            }
            else {
                let message = JSON.parse(xhr.responseText)
                // check relogin attr  
                if (message['relogin']) {
                    document.getElementById('login-form').style.visibility='visible'
                    document.getElementById('login-form').style.display='block'
                    document.getElementById('submit-btn-web').style.display = 'none';
                    remove_objects()
                    Telegram.WebApp.MainButton.disable();
                    localStorage.removeItem('session');
                }
                create_notif(message['error'], 'danger')
            }
            Telegram.WebApp.MainButton.hideProgress();
        }
    };
    create_notif('لطفا کمی صبر کنید...', 'warning')
    xhr.send(params);
    // Telegram.WebApp.close()
}

function create_notif(message, type) {
    let alert_obj = document.getElementById('success-alert')
    alert_obj.style.display = 'block'
    alert_obj.className = 'alert alert-' + type
    $('#request-alert-message').text(message);

    setTimeout(function(param){
        alert_obj.style.display = 'none'
    }.bind(null), 5000);
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
    let session = localStorage.getItem('session');
    Telegram.WebApp.MainButton.showProgress(true);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", `${origin}api/v1/get-food-list/`, true);
    params = `session=${session}`
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE) {

            if (this.status === 200) {
                let message = JSON.parse(xhr.responseText)['food_list']

                food_list = message;
                document.getElementsByClassName('navbar-container')[0].style.visibility='visible';
                $('#user-name').text(food_list['name']);
                $('#user-credit').text("اعتبار: " + pretty_numbers(food_list['credit']) + " تومان");
                $('#user-credit').attr('value', food_list['credit'])
                create_days()
                if (!Object.keys(initDataUnsafe).length) {
                    document.getElementById('submit-btn-web').style.display = 'block';
                }
            }
            else {
                let message = JSON.parse(xhr.responseText)
                // check relogin attr  
                if (message['relogin']) {
                    document.getElementById('login-form').style.visibility='visible'
                    document.getElementById('login-form').style.display='block'
                    document.getElementById('submit-btn-web').style.display = 'none';
                    Telegram.WebApp.MainButton.disable();
                    remove_objects()
                    localStorage.removeItem('session');
                }
                create_notif(message['error'], 'danger')
            }
            Telegram.WebApp.MainButton.hideProgress();
        }
    };
    create_notif('لطفا کمی صبر کنید...', 'warning')
    xhr.send(params);
}

function chek_login() {
    // get session from local storage
    let session = localStorage.getItem('session');
    if (session == null) {
        // login
        document.getElementById('login-form').style.visibility='visible'
        document.getElementById('login-form').style.display='block'
        Telegram.WebApp.MainButton.disable();
    }
    else {
        // get food list
        login_and_place_list()
    }
}

function login_button_clicked() {
    let student_number = document.getElementById('student_number').value;
    let student_password = document.getElementById('student_password').value;
    get_session_from_api(student_number, student_password)
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
    Telegram.WebApp.MainButton.showProgress(true);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", `${origin}api/v1/login/`, true);
    params = `stun=${username}&password=${password}`
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE) {

            if (this.status === 200) {
                let response = JSON.parse(xhr.responseText)
                let session = response['session']
                localStorage.setItem('session', session)
                let message = response['message']
                document.getElementById('login-form').style.visibility='hidden'
                document.getElementById('login-form').style.display='none'
                login_and_place_list()
                Telegram.WebApp.MainButton.enable();
                create_notif(message, 'success')
            }
            else {
                let message = JSON.parse(xhr.responseText)
                if (message['relogin']) {
                    Telegram.WebApp.MainButton.disable();
                    document.getElementById('login-form').style.visibility='visible'
                    document.getElementById('login-form').style.display='block'
                    document.getElementById('submit-btn-web').style.display = 'none';
                    remove_objects()
                    localStorage.removeItem('session');
                }
                create_notif(message['error'], 'danger')
            }
            Telegram.WebApp.MainButton.hideProgress();
        }
    };
    create_notif('لطفا کمی صبر کنید...', 'warning')
    xhr.send(params);
}

Telegram.WebApp.MainButton.disable();
chek_login()