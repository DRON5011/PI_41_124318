--
-- PostgreSQL database dump
--

\restrict 8rORrcod1Yee9AW7n2o6lAEGVLzmMfWQdXmNwRagBS2Le63r8iChr6FeI2nfiQG

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg13+1)
-- Dumped by pg_dump version 18.3 (Debian 18.3-1.pgdg13+1)

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
    status text DEFAULT '╨Ч╨░╨┐╨╗╨░╨╜╨╕╤А╨╛╨▓╨░╨╜╨░'::text,
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
    status text DEFAULT '╨Э╨╡╨╛╨▒╤А╨░╨▒╨╛╤В╨░╨╜╨░'::text
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
4	2026-03-18 13:17:44	2026-03-18 13:17:44	ussu0257gfhob92y	ussu0257gfhob92y	4	╨Я╨╗╨░╨╜ ╤А╨░╤Б╤Е╨╛╨┤╨╛╨▓	╨н╨║╨╛╨╜╨╛╨╝╨╕╨║╨░	2026-03-11	10:40:00	12:10:00	╨Ч╨░╨┐╨╗╨░╨╜╨╕╤А╨╛╨▓╨░╨╜╨░	\N	2
2	2026-03-18 13:16:08	2026-03-18 13:17:57	ussu0257gfhob92y	ussu0257gfhob92y	2	╨Я╤А╨╛╨│╤А╨░╨╝╨╝╨╕╤А╨╛╨▓╨░╨╜╨╕╨╡ C++ 2	╨Я╤А╨╛╨│╤А╨░╨╝╨╝╨╕╤А╨╛╨▓╨░╨╜╨╕╨╡	2026-03-10	09:00:00	10:30:00	╨Ю╤В╨╝╨╡╨╜╨╡╨╜╨░	\N	1
1	2026-03-18 13:15:32	2026-03-18 13:19:15	ussu0257gfhob92y	ussu0257gfhob92y	1	╨Я╤А╨╛╨│╤А╨░╨╝╨╝╨╕╤А╨╛╨▓╨░╨╜╨╕╨╡ C++	╨Я╤А╨╛╨│╤А╨░╨╝╨╝╨╕╤А╨╛╨▓╨░╨╜╨╕╨╡	2026-03-03	09:00:00	10:30:00	╨Я╤А╨╛╨▓╨╡╨┤╨╡╨╜╨░	1	1
3	2026-03-18 13:17:09	2026-03-18 13:20:07	ussu0257gfhob92y	ussu0257gfhob92y	3	╨Я╨╗╨░╨╜ ╨┐╤А╨╛╨┤╨░╨╢	╨н╨║╨╛╨╜╨╛╨╝╨╕╨║╨░	2026-03-04	10:40:00	12:10:00	╨Я╤А╨╛╨▓╨╡╨┤╨╡╨╜╨░	2	2
\.


--
-- Data for Name: Metaphors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Metaphors" (id, created_at, updated_at, created_by, updated_by, nc_order, short_name, texted_audio, start_time, end_time, "Teachers_id", "Records_id") FROM stdin;
1	2026-03-18 13:22:18	2026-03-18 13:22:18	ussu0257gfhob92y	ussu0257gfhob92y	1	╨г╨┤╨░╤З╨╜╤Л╨╣ ╨┐╤А╨╕╨╝╨╡╤А	\N	01:00:00	01:04:00	2	2
\.


--
-- Data for Name: Problem_marks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Problem_marks" (id, created_at, updated_at, created_by, updated_by, nc_order, short_name, "desc", "time", "Students_id", "Records_id") FROM stdin;
1	2026-03-18 13:21:43	2026-03-18 13:21:43	ussu0257gfhob92y	ussu0257gfhob92y	1	╨У╤А╨╛╨╝╨╛╨╖╨┤╨║╨╛╨╡ ╨╛╨┐╨╕╤Б╨░╨╜╨╕╨╡	╨б╨╗╨╕╤И╨║╨╛╨╝ ╨╝╨╜╨╛╨│╨╛ ╨╛╨▒ ╨╛╨┤╨╜╨╛╨╝ ╨╕ ╤В╨╛╨╝ ╨╢╨╡, ╨┐╨╛╤В╨╡╤А╤П ╤Д╨╛╨║╤Г╤Б╨░ ╨▓╨╜╨╕╨╝╨░╨╜╨╕╤П ╨░╤Г╨┤╨╕╤В╨╛╤А╨╕╨╕	00:30:00	1	1
\.


--
-- Data for Name: Records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Records" (id, created_at, updated_at, created_by, updated_by, nc_order, file_name, url_audio, url_texted_audio, url_conspect, status) FROM stdin;
1	2026-03-18 13:19:15	2026-03-18 13:21:43	ussu0257gfhob92y	ussu0257gfhob92y	1	╨Я╤А╨╛╨│╤А╨░╨╝╨╝╨╕╤А╨╛╨▓╨░╨╜╨╕╨╡ C++ 1	https://╨б╤Б╤Л╨╗╨║╨░1.1.su	\N	\N	╨Э╨╡╨╛╨▒╤А╨░╨▒╨╛╤В╨░╨╜╨░
2	2026-03-18 13:20:07	2026-03-18 13:22:18	ussu0257gfhob92y	ussu0257gfhob92y	2	╨Я╨╗╨░╨╜ ╨┐╤А╨╛╨┤╨░╨╢	https://╨б╤Б╤Л╨╗╨║╨░2.1.su	\N	\N	╨Э╨╡╨╛╨▒╤А╨░╨▒╨╛╤В╨░╨╜╨░
\.


--
-- Data for Name: Students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Students" (id, created_at, updated_at, created_by, updated_by, nc_order, fio, email, password) FROM stdin;
2	2026-03-18 13:13:50	\N	ussu0257gfhob92y	\N	2	╨Ъ╤Г╨╖╨╜╨╡╤Ж╨╛╨▓╨░ ╨Х╨╗╨╡╨╜╨░ ╨Э╨╕╨║╨╛╨╗╨░╨╡╨▓╨╜╨░	Test2@test.ru	4567
3	2026-03-18 13:14:16	\N	ussu0257gfhob92y	\N	3	╨б╨╛╨╗╨╛╨╝╨╛╨╜╨╛╨▓ ╨Р╤А╨╡╨╣ ╨Р╤А╨╕╨╝╨╛╨▓╨╕╤З	Test3@test.ru	6789
1	2026-03-18 13:13:18	2026-03-18 13:21:43	ussu0257gfhob92y	ussu0257gfhob92y	1	╨Т╨░╤Б╨╕╨╗╤М╨╡╨▓ ╨б╤В╨╡╨┐╨░╨╜ ╨Э╨╕╨║╨╛╨╗╨░╨╡╨▓╨╕╤З	Test1@test.ru	3456
\.


--
-- Data for Name: Teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Teachers" (id, created_at, updated_at, created_by, updated_by, nc_order, fio, email, password) FROM stdin;
1	2026-03-18 13:12:13	2026-03-18 13:16:08	ussu0257gfhob92y	ussu0257gfhob92y	1	╨Ш╨▓╨░╨╜╨╛╨▓ ╨Ш╨▓╨░╨╜ ╨Ш╨▓╨░╨╜╤Л╤З	test1@test.ru	1234
2	2026-03-18 13:12:42	2026-03-18 13:22:18	ussu0257gfhob92y	ussu0257gfhob92y	2	╨Я╤А╨╛╤Е╨╛╤А╨╛╨▓ ╨Я╤С╤В╤А ╨Ъ╤Г╨╖╤М╨╝╨╕╤З	test2@test.ru	2345
\.


--
-- Name: Lections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Lections_id_seq"', 4, true);


--
-- Name: Metaphors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Metaphors_id_seq"', 1, true);


--
-- Name: Problem_marks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Problem_marks_id_seq"', 1, true);


--
-- Name: Records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Records_id_seq"', 2, true);


--
-- Name: Students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Students_id_seq"', 3, true);


--
-- Name: Teachers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Teachers_id_seq"', 2, true);


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

\unrestrict 8rORrcod1Yee9AW7n2o6lAEGVLzmMfWQdXmNwRagBS2Le63r8iChr6FeI2nfiQG

