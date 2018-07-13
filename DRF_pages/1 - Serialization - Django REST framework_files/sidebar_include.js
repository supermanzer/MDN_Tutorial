var include = '';



include += '<a href="http://saucelabs.com?utm_campaign=sponsorship&amp;utm_medium=logo&amp;utm_source=django-rest">';
include += '<img width="130px" src="https://fund-rest-framework.s3.amazonaws.com/Sauce_Lab_Logo_130x130.png"></img>';
include += '</a>';


include += '<p><a class="promo" href="http://saucelabs.com?utm_campaign=sponsorship&amp;utm_medium=logo&amp;utm_source=django-rest">Sauce Labs provides the world’s largest cloud-based platform for the automated testing of web and mobile applications. Deploy with confidence across hundreds of browser / OS platforms. Free trial!</a></p>';



include += '<p><a href="https://fund.django-rest-framework.org/topics/funding/">Fund Django REST framework</a></p>'

document.getElementById('sidebarInclude').innerHTML = include;
