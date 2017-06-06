function FeatureFormModel() {
    var self = this;

    this.PRODUCT_AREAS = [
        "Policies", "Billing", "Claims", "Reports",
    ];
    this.CLIENTS = ko.observableArray([]);

    $.getJSON("/api/clients", function(data) {
        self.CLIENTS(data);
    });

    this.title = ko.observable();
    this.description = ko.observable();
    this.client = ko.observable(); 
    this.priority = ko.observable(1);
    this.targetDate = ko.observable();
    this.productArea = ko.observable();
    this.errors = ko.observableArray();

    this.clear = function() {
        var today = JSON.stringify(new Date()).split("T")[0].substr(1);
        self.title(null);
        self.description(null);
        self.client(null);
        self.priority(1);
        self.targetDate(today);
        self.productArea(null);
        self.errors();
    };

    this.clear();

    this.addFeatureRequest = function() {
        var data = ko.toJSON({
            title: self.title,
            description: self.description,
            client_id: self.client().id,
            priority: self.priority,
            target_date: self.targetDate,
            product_area: self.productArea,
        });

        console.log(data);
        $.post("/api/features", data, function(data) {
            self.clear();
            console.log("Success: ", data);
        }).fail(function(err) {
            resp = $.parseJSON(err.responseText);
            console.log("Response: ", resp);

            var mappedErrors = $.map(resp.errors, function(value, key) {
                return $.map(value, function(v) {
                    return {"text": key + ": " + v};
                });
            });
            self.errors(mappedErrors);
            console.log("Mapped Errors: " + mappedErrors);
        });
    };
}

ko.applyBindings(new FeatureFormModel());
