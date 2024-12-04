create table if not exists public.teachers (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name varchar(500) not null,
    phone char(12) null,
    email varchar(100) null,
    comment text null
);

create table if not exists public.variants (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    teacher_id bigint not null references teachers(id),
    title varchar(200) not null,
    created_at timestamp not null default now()
);

create table if not exists public.tests (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    teacher_id bigint null references teachers(id),
    name varchar(200) not null,
    content text not null
);

create table if not exists public.tests_variants (
    test_id bigint not null references tests(id),
    variant_id bigint not null references variants(id),
    number int null,
    unique(test_id, variant_id)
);