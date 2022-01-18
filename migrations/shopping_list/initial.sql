create table shopping_list (
    id serial primary key,
    item1 int,
    item2 int,
    item3 int,
    status VARCHAR(32) NOT NULL,
    created_by int,
    allow_multiple_shoppers boolean,
    constraint fk_item1 foreign key (item1) references shopping_item(id),
    constraint fk_item2 foreign key (item2) references shopping_item(id),
    constraint fk_item3 foreign key (item3) references shopping_item(id),
    constraint fk_created_by foreign key (created_by) references registered_user(id)
)