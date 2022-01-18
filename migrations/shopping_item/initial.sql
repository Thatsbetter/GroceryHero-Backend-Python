create table shopping_item (
    id serial primary key,
    product varchar(128) not null,
    count integer not null,
    shopper int,
    status varchar(32),
    constraint fk_shopper foreign key (shopper) references registered_user(id)
)
