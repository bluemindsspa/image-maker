odoo.define("account_accountant_renconcile_all.reconciliation_validate_all", (require) => {
    "use strict";

    const ReconciliationClientAction = require("account.ReconciliationClientAction");
    const Widget = require("web.Widget");
    const core = require("web.core");
    const QWeb = core.qweb;

    ReconciliationClientAction.StatementAction.include({
        events: {
            "click .oe_validate_all": "_onclick",
        },
        _onclick: function (ev) {
            this.trigger_up("validate");
        },
    });

});