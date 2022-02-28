

insert into role (name) values ('anonymous'),('admin'),('editor');

insert into users (first_name,last_name,password,email) values ('Admin','BEIS-Person','Password1!','admin@beis.gov.uk');
insert into users (first_name,last_name,password,email) values ('Editor','BEIS-Person','Password1!','editor@beis.gov.uk');
insert into users (first_name,last_name,password,email) values ('Anonymous','BEIS-Person','Password1!','anonymous@beis.gov.uk');

insert into user_role (user_id,role_id) values ((select id from users where email = 'admin@beis.gov.uk'),(select id from role where name = 'admin'));
insert into user_role (user_id,role_id) values ((select id from users where email = 'editor@beis.gov.uk'),(select id from role where name = 'editor'));
insert into user_role (user_id,role_id) values ((select id from users where email = 'anonymous@beis.gov.uk'),(select id from role where name = 'anonymous'));

insert into role_actions (action_name,role_id) values ('enrichment_feedback_read',(select id from role where name = 'admin'));
insert into role_actions (action_name,role_id) values ('document_enrichment_feedback_status_read',(select id from role where name = 'admin'));
insert into role_actions (action_name,role_id) values ('enrichment_feedback_read',(select id from role where name = 'editor'));
insert into role_actions (action_name,role_id) values ('document_enrichment_feedback_status_read',(select id from role where name = 'editor'));
insert into role_actions (action_name,role_id) values ('enrichment_feedback_create',(select id from role where name = 'editor'));
insert into role_actions (action_name,role_id) values ('manual_enrichment_create',(select id from role where name = 'editor'));
insert into role_actions (action_name,role_id) values ('document_enrichment_feedback_status_create',(select id from role where name = 'editor'));
