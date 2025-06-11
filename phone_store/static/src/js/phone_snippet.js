odoo.define('phone_store.phone_snippet', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.PhoneStoreSnippet = publicWidget.Widget.extend({
        selector: '.s_text[data-snippet="phone_store.dynamic_snippet"]',
        start: function () {
            var self = this;
            self.$('#phone-promo-list').empty();
            this._rpc({
                route: '/phone-store/promotions',
                params: {},
            }).then(function (data) {
                if (data.length) {
                    data.forEach(function (phone) {
                        self.$('#phone-promo-list').append(
                            `<div class="col-md-4 mb-3">
                                <div class="card p-3 shadow-sm">
                                    <h4>${phone.name}</h4>
                                    <p>Price: $${phone.price}</p>
                                </div>
                            </div>`
                        );
                    });
                } else {
                    self.$('#phone-promo-list').html('<p>No promotions available.</p>');
                }
            });
            return this._super.apply(this, arguments);
        }
    });

});
        