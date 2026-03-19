--
-- PostgreSQL database dump
--

\restrict AAodtcd8F0PFF1o9YqJpIJuvzz8reb1UVtd2IkiFIXphCClPqr479RA39ki7K4g

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg12+1)
-- Dumped by pg_dump version 18.3 (Debian 18.3-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Lections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Lections" (
    id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying,
    updated_by character varying,
    nc_order numeric,
    lection_name text,
    course_name text,
    lection_date date,
    start_time time without time zone DEFAULT '09:00:00'::time without time zone,
    end_time time without time zone DEFAULT '10:30:00'::time without time zone,
    status text DEFAULT '??????????????????????????'::text,
    "Records_id" integer,
    "Teachers_id" integer
);


ALTER TABLE public."Lections" OWNER TO postgres;

--
-- Name: Lections_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Lections_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Lections_id_seq" OWNER TO postgres;

--
-- Name: Lections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Lections_id_seq" OWNED BY public."Lections".id;


--
-- Name: Metaphors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Metaphors" (
    id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying,
    updated_by character varying,
    nc_order numeric,
    short_name text,
    texted_audio text,
    start_time time without time zone,
    end_time time without time zone,
    "Teachers_id" integer,
    "Records_id" integer
);


ALTER TABLE public."Metaphors" OWNER TO postgres;

--
-- Name: Metaphors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Metaphors_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Metaphors_id_seq" OWNER TO postgres;

--
-- Name: Metaphors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Metaphors_id_seq" OWNED BY public."Metaphors".id;


--
-- Name: Problem_marks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Problem_marks" (
    id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying,
    updated_by character varying,
    nc_order numeric,
    short_name text,
    "desc" text,
    "time" time without time zone,
    "Students_id" integer,
    "Records_id" integer
);


ALTER TABLE public."Problem_marks" OWNER TO postgres;

--
-- Name: Problem_marks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Problem_marks_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Problem_marks_id_seq" OWNER TO postgres;

--
-- Name: Problem_marks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Problem_marks_id_seq" OWNED BY public."Problem_marks".id;


--
-- Name: Records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Records" (
    id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying,
    updated_by character varying,
    nc_order numeric,
    file_name text,
    url_audio text,
    url_texted_audio text,
    url_conspect text,
    status text DEFAULT '????????????????????????'::text
);


ALTER TABLE public."Records" OWNER TO postgres;

--
-- Name: Records_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Records_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Records_id_seq" OWNER TO postgres;

--
-- Name: Records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Records_id_seq" OWNED BY public."Records".id;


--
-- Name: Students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Students" (
    id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying,
    updated_by character varying,
    nc_order numeric,
    fio text,
    email character varying,
    password text
);


ALTER TABLE public."Students" OWNER TO postgres;

--
-- Name: Students_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Students_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Students_id_seq" OWNER TO postgres;

--
-- Name: Students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Students_id_seq" OWNED BY public."Students".id;


--
-- Name: Teachers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Teachers" (
    id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying,
    updated_by character varying,
    nc_order numeric,
    fio text,
    email character varying,
    password text
);


ALTER TABLE public."Teachers" OWNER TO postgres;

--
-- Name: Teachers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Teachers_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Teachers_id_seq" OWNER TO postgres;

--
-- Name: Teachers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Teachers_id_seq" OWNED BY public."Teachers".id;


--
-- Name: Lections id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Lections" ALTER COLUMN id SET DEFAULT nextval('public."Lections_id_seq"'::regclass);


--
-- Name: Metaphors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Metaphors" ALTER COLUMN id SET DEFAULT nextval('public."Metaphors_id_seq"'::regclass);


--
-- Name: Problem_marks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Problem_marks" ALTER COLUMN id SET DEFAULT nextval('public."Problem_marks_id_seq"'::regclass);


--
-- Name: Records id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Records" ALTER COLUMN id SET DEFAULT nextval('public."Records_id_seq"'::regclass);


--
-- Name: Students id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Students" ALTER COLUMN id SET DEFAULT nextval('public."Students_id_seq"'::regclass);


--
-- Name: Teachers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Teachers" ALTER COLUMN id SET DEFAULT nextval('public."Teachers_id_seq"'::regclass);


--
-- Data for Name: Lections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Lections" (id, created_at, updated_at, created_by, updated_by, nc_order, lection_name, course_name, lection_date, start_time, end_time, status, "Records_id", "Teachers_id") FROM stdin;
1	2026-03-18 13:15:32	2026-03-19 11:49:12	ussu0257gfhob92y	ussu0257gfhob92y	1	Программирование C++	Программирование	2026-03-03	09:00:00	10:30:00	Проведена	1	1
9	2026-03-19 21:07:09	2026-03-19 21:09:14	ussu0257gfhob92y	ussu0257gfhob92y	8	Теория чисел 2	Высшая математика	2026-03-13	09:00:00	10:30:00	Проведена	\N	6
10	2026-03-19 21:08:02	2026-03-19 21:09:16	ussu0257gfhob92y	ussu0257gfhob92y	9	Теория чисел 3	Высшая математика	2026-03-20	09:00:00	10:30:00	Запланирована	\N	6
12	2026-03-19 21:09:03	2026-03-19 21:09:18	ussu0257gfhob92y	ussu0257gfhob92y	11	Тестирование Pytest2	Тестирование	2026-03-20	10:00:00	11:30:00	Запланирована	\N	5
5	2026-03-19 12:00:39	2026-03-19 12:01:49	ussu0257gfhob92y	ussu0257gfhob92y	5	Теория программирования Python	Программирование	2026-03-11	13:30:00	15:00:00	Отменена	\N	1
6	2026-03-19 12:01:30	2026-03-19 12:02:33	ussu0257gfhob92y	ussu0257gfhob92y	6	Экономический план	Экономика	2026-03-12	09:00:00	10:30:00	Проведена	3	2
8	2026-03-19 21:06:36	2026-03-19 21:10:15	ussu0257gfhob92y	ussu0257gfhob92y	7	Теория чисел	Высшая математика	2026-03-06	09:00:00	10:30:00	Отменена	4	6
2	2026-03-18 13:16:08	2026-03-19 11:50:23	ussu0257gfhob92y	ussu0257gfhob92y	2	Программирование C++ 2	Программирование	2026-03-10	09:00:00	10:30:00	Отменена	\N	1
3	2026-03-18 13:17:09	2026-03-19 11:50:24	ussu0257gfhob92y	ussu0257gfhob92y	3	План продаж	Экономика	2026-03-04	10:40:00	12:10:00	Проведена	2	2
4	2026-03-18 13:17:44	2026-03-19 11:50:26	ussu0257gfhob92y	ussu0257gfhob92y	4	План закупок	Экономика	2026-03-11	10:40:00	12:10:00	Запланирована	\N	2
11	2026-03-19 21:08:39	2026-03-19 21:10:53	ussu0257gfhob92y	ussu0257gfhob92y	10	Тестирование Pytest	Тестерование	2026-03-13	09:00:00	10:30:00	Отменена	5	5
\.


--
-- Data for Name: Metaphors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Metaphors" (id, created_at, updated_at, created_by, updated_by, nc_order, short_name, texted_audio, start_time, end_time, "Teachers_id", "Records_id") FROM stdin;
1	2026-03-18 13:22:18	2026-03-19 11:54:09	ussu0257gfhob92y	ussu0257gfhob92y	1	Удачный пример	\N	01:00:00	01:04:00	2	2
2	2026-03-19 21:13:20	2026-03-19 21:13:20	ussu0257gfhob92y	ussu0257gfhob92y	2	Хороший пример	\N	10:16:00	10:25:00	5	5
3	2026-03-19 21:14:04	2026-03-19 21:14:04	ussu0257gfhob92y	ussu0257gfhob92y	3	Правильный пример	\N	09:20:00	09:25:00	6	4
\.


--
-- Data for Name: Problem_marks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Problem_marks" (id, created_at, updated_at, created_by, updated_by, nc_order, short_name, "desc", "time", "Students_id", "Records_id") FROM stdin;
1	2026-03-18 13:21:43	2026-03-19 11:53:52	ussu0257gfhob92y	ussu0257gfhob92y	1	Громоздкое описание	Слишком много воды	00:30:00	1	1
2	2026-03-19 21:11:53	2026-03-19 21:11:53	ussu0257gfhob92y	ussu0257gfhob92y	2	Плохое объяснение	Недостаточно расписал методы тестирования	09:15:00	4	5
3	2026-03-19 21:12:46	2026-03-19 21:12:46	ussu0257gfhob92y	ussu0257gfhob92y	3	Непонятный термин	Термин что был плохо объяснён на лекции	09:16:00	6	4
\.


--
-- Data for Name: Records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Records" (id, created_at, updated_at, created_by, updated_by, nc_order, file_name, url_audio, url_texted_audio, url_conspect, status) FROM stdin;
1	2026-03-18 13:19:15	2026-03-19 11:51:05	ussu0257gfhob92y	ussu0257gfhob92y	1	Программирование C++ 1	https://Ссылка1.1.su	\N	\N	Необработана
2	2026-03-18 13:20:07	2026-03-19 11:51:07	ussu0257gfhob92y	ussu0257gfhob92y	2	План продаж	https://Ссылка2.1.su	\N	\N	Необработана
3	2026-03-19 12:01:58	2026-03-19 12:02:33	ussu0257gfhob92y	ussu0257gfhob92y	3	Экономический план	https://Ссылка3.1.su	\N	\N	Необработана
5	2026-03-19 21:10:53	2026-03-19 21:13:20	ussu0257gfhob92y	ussu0257gfhob92y	5	Тестирование 1	https://Ссылка5.ru	\N	\N	Необработана
4	2026-03-19 21:10:15	2026-03-19 21:14:04	ussu0257gfhob92y	ussu0257gfhob92y	4	Файл 1	https://Ссылка4.ru	\N	\N	Необработана
\.


--
-- Data for Name: Students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Students" (id, created_at, updated_at, created_by, updated_by, nc_order, fio, email, password) FROM stdin;
1	2026-03-18 13:13:18	2026-03-19 11:53:02	ussu0257gfhob92y	ussu0257gfhob92y	1	Васильев Степан Николаевич	Test1@test.ru	3456
2	2026-03-18 13:13:50	2026-03-19 11:53:13	ussu0257gfhob92y	ussu0257gfhob92y	2	Кузнецова Елена Николаевна	Test2@test.ru	4567
3	2026-03-18 13:14:16	2026-03-19 11:53:24	ussu0257gfhob92y	ussu0257gfhob92y	3	Соломонов Арей Аримович	Test3@test.ru	6789
5	2026-03-19 21:05:04	2026-03-19 21:05:43	ussu0257gfhob92y	ussu0257gfhob92y	5	Тихонов Павел Андреевич	Test5@test.ru	7837
4	2026-03-19 21:04:38	2026-03-19 21:11:53	ussu0257gfhob92y	ussu0257gfhob92y	4	Иванов Иван Иваныч	Test4@test.ru	6732
6	2026-03-19 21:05:37	2026-03-19 21:12:46	ussu0257gfhob92y	ussu0257gfhob92y	6	Ларинова Анна Сергеевна	Test6@test.ru	3753
\.


--
-- Data for Name: Teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Teachers" (id, created_at, updated_at, created_by, updated_by, nc_order, fio, email, password) FROM stdin;
1	2026-03-18 13:12:13	2026-03-19 12:01:25	ussu0257gfhob92y	ussu0257gfhob92y	1	Иванов Иван Иваныч	test1@test.ru	1234
2	2026-03-18 13:12:42	2026-03-19 12:01:56	ussu0257gfhob92y	ussu0257gfhob92y	2	Прохоров Пётр Кузьмич	test2@test.ru	2345
3	2026-03-19 21:02:11	2026-03-19 21:02:40	ussu0257gfhob92y	ussu0257gfhob92y	3	Дроздов Павел Валерьевич	test3@test.ru	3456
5	2026-03-19 21:03:17	2026-03-19 21:13:20	ussu0257gfhob92y	ussu0257gfhob92y	4	Трофимов Игорь Смирновский	test4@test.ru	8498
6	2026-03-19 21:03:45	2026-03-19 21:14:04	ussu0257gfhob92y	ussu0257gfhob92y	5	Елисеева Вероника Макаровна	test5@test.ru	9971
\.


--
-- Name: Lections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Lections_id_seq"', 12, true);


--
-- Name: Metaphors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Metaphors_id_seq"', 3, true);


--
-- Name: Problem_marks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Problem_marks_id_seq"', 3, true);


--
-- Name: Records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Records_id_seq"', 5, true);


--
-- Name: Students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Students_id_seq"', 6, true);


--
-- Name: Teachers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Teachers_id_seq"', 6, true);


--
-- Name: Lections Lections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Lections"
    ADD CONSTRAINT "Lections_pkey" PRIMARY KEY (id);


--
-- Name: Metaphors Metaphors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Metaphors"
    ADD CONSTRAINT "Metaphors_pkey" PRIMARY KEY (id);


--
-- Name: Problem_marks Problem_marks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Problem_marks"
    ADD CONSTRAINT "Problem_marks_pkey" PRIMARY KEY (id);


--
-- Name: Records Records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Records"
    ADD CONSTRAINT "Records_pkey" PRIMARY KEY (id);


--
-- Name: Students Students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Students"
    ADD CONSTRAINT "Students_pkey" PRIMARY KEY (id);


--
-- Name: Teachers Teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Teachers"
    ADD CONSTRAINT "Teachers_pkey" PRIMARY KEY (id);


--
-- Name: Lections uk_Lections_Records_id_l1mull; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Lections"
    ADD CONSTRAINT "uk_Lections_Records_id_l1mull" UNIQUE ("Records_id");


--
-- Name: Lections_order_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Lections_order_idx" ON public."Lections" USING btree (nc_order);


--
-- Name: Metaphors_order_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Metaphors_order_idx" ON public."Metaphors" USING btree (nc_order);


--
-- Name: Problem_marks_order_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Problem_marks_order_idx" ON public."Problem_marks" USING btree (nc_order);


--
-- Name: Records_order_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Records_order_idx" ON public."Records" USING btree (nc_order);


--
-- Name: Students_order_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Students_order_idx" ON public."Students" USING btree (nc_order);


--
-- Name: Teachers_order_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Teachers_order_idx" ON public."Teachers" USING btree (nc_order);


--
-- Name: fk_Records_Lections_b38cvrclt1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fk_Records_Lections_b38cvrclt1" ON public."Lections" USING btree ("Records_id");


--
-- Name: fk_Records_Metaphors_8lgod8kims; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fk_Records_Metaphors_8lgod8kims" ON public."Metaphors" USING btree ("Records_id");


--
-- Name: fk_Records_Problem_ma_jdkkysnm5n; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fk_Records_Problem_ma_jdkkysnm5n" ON public."Problem_marks" USING btree ("Records_id");


--
-- Name: fk_Students_Problem_ma_w_pez_g7h4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fk_Students_Problem_ma_w_pez_g7h4" ON public."Problem_marks" USING btree ("Students_id");


--
-- Name: fk_Teachers_Lections_k99rmwfya4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fk_Teachers_Lections_k99rmwfya4" ON public."Lections" USING btree ("Teachers_id");


--
-- Name: fk_Teachers_Metaphors_y5yxt526k5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fk_Teachers_Metaphors_y5yxt526k5" ON public."Metaphors" USING btree ("Teachers_id");


--
-- Name: Lections fk_Records_Lections_tlv84c3zbj; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Lections"
    ADD CONSTRAINT "fk_Records_Lections_tlv84c3zbj" FOREIGN KEY ("Records_id") REFERENCES public."Records"(id);


--
-- Name: Metaphors fk_Records_Metaphors_6zxnn87o_l; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Metaphors"
    ADD CONSTRAINT "fk_Records_Metaphors_6zxnn87o_l" FOREIGN KEY ("Records_id") REFERENCES public."Records"(id);


--
-- Name: Problem_marks fk_Records_Problem_ma_nvw2pn65bx; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Problem_marks"
    ADD CONSTRAINT "fk_Records_Problem_ma_nvw2pn65bx" FOREIGN KEY ("Records_id") REFERENCES public."Records"(id);


--
-- Name: Problem_marks fk_Students_Problem_ma_zmy7grmx20; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Problem_marks"
    ADD CONSTRAINT "fk_Students_Problem_ma_zmy7grmx20" FOREIGN KEY ("Students_id") REFERENCES public."Students"(id);


--
-- Name: Lections fk_Teachers_Lections_wint7ryj7c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Lections"
    ADD CONSTRAINT "fk_Teachers_Lections_wint7ryj7c" FOREIGN KEY ("Teachers_id") REFERENCES public."Teachers"(id);


--
-- Name: Metaphors fk_Teachers_Metaphors_pzj20rco42; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Metaphors"
    ADD CONSTRAINT "fk_Teachers_Metaphors_pzj20rco42" FOREIGN KEY ("Teachers_id") REFERENCES public."Teachers"(id);


--
-- PostgreSQL database dump complete
--

\unrestrict AAodtcd8F0PFF1o9YqJpIJuvzz8reb1UVtd2IkiFIXphCClPqr479RA39ki7K4g

