let current_val= [];
const autocomplete = new MultiSelect2(".autocomplete", {
    options: myOptions,
    value: [],
    placeholder: "filter object",
    multiple: true,
    autocomplete: true,
    icon: "fa fa-times",
    onChange: value => {
        console.log(value);
        current_val=value;
        console.log(current_val)
    },
});
