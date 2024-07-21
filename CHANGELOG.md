# Changelog

---
## [2.3.5](https://github.com/tmlmt/milk-tracker/compare/v2.3.4..v2.3.5) - 2024-07-21

### 🩹 Fixes

- **(systemd)** install target - ([1d4ca30](https://github.com/tmlmt/milk-tracker/commit/1d4ca3057351d6c1c60b31936674bb1036e8b53b)) - Thomas Lamant

---
## [2.3.4](https://github.com/tmlmt/milk-tracker/compare/v2.3.3..v2.3.4) - 2024-07-14

### 🩹 Fixes

- **(days_between_txt)** wrong calculations when the later date is in January - ([a7182bf](https://github.com/tmlmt/milk-tracker/commit/a7182bf907e517b7a328b44f578ac03a3158784f)) - Thomas Lamant

### 🏡 Chore

- **(README)** update screenshots - ([d579a7b](https://github.com/tmlmt/milk-tracker/commit/d579a7b0c9f261ec559acfca25488cd4904b9652)) - Thomas Lamant
- pre-add Memories screenshot - ([cee2437](https://github.com/tmlmt/milk-tracker/commit/cee2437249b0b8f04d455693c1ab98e99a169b5f)) - Thomas Lamant

---
## [2.3.3](https://github.com/tmlmt/milk-tracker/compare/v2.3.2..v2.3.3) - 2024-07-14

### 🩹 Fixes

- don't overwrite memories asset file when upgrading - ([40c48d5](https://github.com/tmlmt/milk-tracker/commit/40c48d5afd36b7b16ef8d078c6f53b4643311107)) - Thomas Lamant

### 🏡 Chore

- update README - ([12df800](https://github.com/tmlmt/milk-tracker/commit/12df800d4b10efac7ca2070be6c50c957b0c4ea4)) - Thomas Lamant

---
## [2.3.2](https://github.com/tmlmt/milk-tracker/compare/v2.3.1..v2.3.2) - 2024-07-14

### 🎨 Style

- align burger menu with title - ([c7c79b3](https://github.com/tmlmt/milk-tracker/commit/c7c79b366a9bc09406cb7a4511e0bf7e0e7bf78d)) - Thomas Lamant

---
## [2.3.1](https://github.com/tmlmt/milk-tracker/compare/v2.3.0..v2.3.1) - 2024-07-14

### 🩹 Fixes

- app crashes when it was last locked with an ongoing meal more than 100 hrs ago - ([75a5550](https://github.com/tmlmt/milk-tracker/commit/75a5550b4c2b53e5f4f6a0d135fe6d8721563b5a)) - Thomas Lamant

### 🎨 Style

- improve time_utils and tests - ([585267e](https://github.com/tmlmt/milk-tracker/commit/585267e4c265507e9ecd5216d3b64c6e135e0248)) - Thomas Lamant
- resolve most ruff warnings - ([3119845](https://github.com/tmlmt/milk-tracker/commit/3119845310c7c4fc65faa5345b3655c6d0342a6d)) - Thomas Lamant

### 🤖 CI

- fix coverage workflow - ([e6638a0](https://github.com/tmlmt/milk-tracker/commit/e6638a0caced0c58879d941c7601aa77cb4a48bb)) - Thomas Lamant

### 🏡 Chore

- **(coverage)** update badge - ([38f3cb5](https://github.com/tmlmt/milk-tracker/commit/38f3cb5b727b8e105662f4d98da223dbd8221f16)) - github-actions[bot]
- **(deps)** fix inline-snapshot in env file - ([0155431](https://github.com/tmlmt/milk-tracker/commit/0155431f92de980c4212c9bc2b5da222c55bf950)) - Thomas Lamant

---
## [2.3.0](https://github.com/tmlmt/milk-tracker/compare/v2.2.0..v2.3.0) - 2024-07-14

### 🚀 Enhancements

- keep log of daily memories (#22) - ([b0f9afa](https://github.com/tmlmt/milk-tracker/commit/b0f9afa2cc3aa7baef046e88076b3bf17501943d)) - Thomas Lamant

### 🏡 Chore

- **(deps)** remove unused prophets and update all other deps - ([646f4c3](https://github.com/tmlmt/milk-tracker/commit/646f4c37f45e61730ee88477a2baf83bc1a68e8b)) - Thomas Lamant

---
## [2.2.0](https://github.com/tmlmt/milk-tracker/compare/v2.1.0..v2.2.0) - 2024-07-08

### 🚀 Enhancements

- add favicon - ([0ec48fa](https://github.com/tmlmt/milk-tracker/commit/0ec48fa73f09c3546d27fbb62a58c281698036dc)) - Thomas Lamant

### 🩹 Fixes

- first round not showing when starting meal recording - ([bcb8b49](https://github.com/tmlmt/milk-tracker/commit/bcb8b49909e5ad4174a814780b54a2dea02449a8)) - Thomas Lamant

### 🏡 Chore

- **(deps)** update all deps - ([cb85d0f](https://github.com/tmlmt/milk-tracker/commit/cb85d0f4f83730f219e69c3925c514ce7f6d0a38), [1d49ffb](https://github.com/tmlmt/milk-tracker/commit/1d49ffb8c0796ce03cb619c3aca09e430b7c9566)) - Thomas Lamant
- **(format)** reduce line-length to 90 - ([9baa5fd](https://github.com/tmlmt/milk-tracker/commit/9baa5fd6ca3df31977b9b3fdc7105e85a03f77e2)) - Thomas Lamant
- **(time_utils)** pre-add a is_before_end_of_tomorrow function - ([17e7019](https://github.com/tmlmt/milk-tracker/commit/17e7019023303b19d741d271f93ee7d331e8f8a7)) - Thomas Lamant

---
## [2.1.0](https://github.com/tmlmt/milk-tracker/compare/v2.0.1..v2.1.0) - 2024-06-13

### 🚀 Enhancements

- add lock icon in previous start/end when meal is locked - ([619d81f](https://github.com/tmlmt/milk-tracker/commit/619d81fea5d64f23712730f0d8d2d0c5eccae84b)) - Thomas Lamant
- auto focus while typing start and end times of new meal - ([1b5eee6](https://github.com/tmlmt/milk-tracker/commit/1b5eee6cd669d2a80ff78ccde8042fe0a785869d)) - Thomas Lamant

### 🚜 Refactor

- make use of refreshable functions - ([92338bc](https://github.com/tmlmt/milk-tracker/commit/92338bc65114721bd20c322a09b2dfe0ac0dc5de)) - Thomas Lamant

---
## [2.0.1](https://github.com/tmlmt/milk-tracker/compare/v2.0.0..v2.0.1) - 2024-06-12

### 🩹 Fixes

- **(controller)** vitamin checks not updated after day change - ([71f00ef](https://github.com/tmlmt/milk-tracker/commit/71f00ef594d85abfba96ac864cce2239388a61e5)) - Thomas Lamant

### 🤖 CI

- **(cd)** run deploy-app only when we don't deploy-env - ([7bec6ae](https://github.com/tmlmt/milk-tracker/commit/7bec6aee2b9dd4e2a5298832bafb66d0927d78af)) - Thomas Lamant

### 🏡 Chore

- **(README)** add instructions for self-hosting - ([0b142d6](https://github.com/tmlmt/milk-tracker/commit/0b142d6e9d3bd4953ae4e7f7dfdaf99ff74467e0)) - Thomas Lamant

---
## [2.0.0](https://github.com/tmlmt/milk-tracker/compare/v2.0.0-beta.4..v2.0.0) - 2024-06-11

### 🚀 Enhancements

- reminders for vitamin intake - ([ec52212](https://github.com/tmlmt/milk-tracker/commit/ec522127f65346b5a4bb1ca49edcf6653f5085db)) - Thomas Lamant

### 🩹 Fixes

- **(record_meal)** only enable button when meal is ongoing - ([c93ca28](https://github.com/tmlmt/milk-tracker/commit/c93ca2866c5de3cd4ee826a32641db40bec9bee6)) - Thomas Lamant

### 🤖 CI

- **(cd)** run jobs sequentially - ([f1edff0](https://github.com/tmlmt/milk-tracker/commit/f1edff021c5cefb3cb0eb547c0a68cfd737d4a98)) - Thomas Lamant
- **(cd)** switch deploy-end to faster rsync script - ([83e9121](https://github.com/tmlmt/milk-tracker/commit/83e91214c5c9c7adfdbe2ac14c207d45dbb1f2b6)) - Thomas Lamant
- **(coverage)** bump tj-actions/verify-changed-files to v20 - ([ae7ab7a](https://github.com/tmlmt/milk-tracker/commit/ae7ab7a5737e107cc8ea08eb44e6493cf73317f9)) - Thomas Lamant

### 🏡 Chore

- **(cliff)** skip changelog and release commits - ([7cde869](https://github.com/tmlmt/milk-tracker/commit/7cde8695699c4e5f0970fc059e991d79b476cb05)) - Thomas Lamant
- **(coverage)** update badge - ([244f350](https://github.com/tmlmt/milk-tracker/commit/244f35086949bcc85ff06626d1623d3b96e7f3b5)) - github-actions[bot]
- **(pyproject)** add project details as per PEP 621 - ([d7cf92f](https://github.com/tmlmt/milk-tracker/commit/d7cf92fffadb07fea5f07ce838719575c5900679)) - Thomas Lamant
- upload scripts - ([bd13ebe](https://github.com/tmlmt/milk-tracker/commit/bd13ebeb7f922fe67caedaec9e9bf48ee052ed88)) - Thomas Lamant
- update README - ([a62e234](https://github.com/tmlmt/milk-tracker/commit/a62e234b9ed39d25bf08fa14e1ee7966a04534e2)) - Thomas Lamant

---
## [2.0.0-beta.4](https://github.com/tmlmt/milk-tracker/compare/v2.0.0-beta.3..v2.0.0-beta.4) - 2024-06-11

### 🚀 Enhancements

- track and time meal rounds when recording a meal - ([c92b43e](https://github.com/tmlmt/milk-tracker/commit/c92b43eb273fafe4db0e52e9380f6ab50249f074)) - Thomas Lamant

### 🩹 Fixes

- **(schemas)** UpdatableModel does not work with pydantic v2 - ([083e608](https://github.com/tmlmt/milk-tracker/commit/083e6086d92bbf9ec99bcae7356af73f1c2ec134)) - Thomas Lamant
- end time validation fails after adding a meal - ([fc3f1d9](https://github.com/tmlmt/milk-tracker/commit/fc3f1d9bb10ac9b8ade847fabf5ff8e8a3c3ae25)) - Thomas Lamant

### 🚜 Refactor

- split into pages - ([5dc26ee](https://github.com/tmlmt/milk-tracker/commit/5dc26eea78520636fe2e989f5079505fa874d429)) - Thomas Lamant

### 🤖 CI

- optionally (re)deploy environment - ([c719631](https://github.com/tmlmt/milk-tracker/commit/c7196315255cf7ccf218bba207e29cbecc6404bd)) - Thomas Lamant

### 🏡 Chore

- **(coverage)** remove test files from stats - ([ae9dbe2](https://github.com/tmlmt/milk-tracker/commit/ae9dbe2d0b81477b62dc448e9541f2ea4be65101)) - Thomas Lamant
- **(deps)** update all dependencies - ([1ee401e](https://github.com/tmlmt/milk-tracker/commit/1ee401e7868152691d0e32efba82ef4cdd706cd6)) - Thomas Lamant
- remove unused imports and lint - ([0cac7d0](https://github.com/tmlmt/milk-tracker/commit/0cac7d028b634687f450afa70fc46617a6dc4338)) - Thomas Lamant

---
## [2.0.0-beta.3](https://github.com/tmlmt/milk-tracker/compare/v2.0.0-beta.2..v2.0.0-beta.3) - 2024-06-10

### 🚀 Enhancements

- add summary graphs - ([17c6c4c](https://github.com/tmlmt/milk-tracker/commit/17c6c4c93cdf71ce4beb7ad19296b44e3a851588)) - Thomas Lamant

### 🩹 Fixes

- **(force_update)** include update of summary graphs - ([2050625](https://github.com/tmlmt/milk-tracker/commit/2050625dc6101ff24ae7dc97b671109a64bca817)) - Thomas Lamant

### 🚜 Refactor

- move additional css to external file - ([3253bcb](https://github.com/tmlmt/milk-tracker/commit/3253bcb461d17eff5fa62f7ef760e07924584a7f)) - Thomas Lamant

### 🎨 Style

- **(graphs)** consistent use of words and case - ([de56b34](https://github.com/tmlmt/milk-tracker/commit/de56b34b9c20114607e90b46521e8159b7d8951c)) - Thomas Lamant
- **(graphs)** improve responsiveness - ([d9e1fce](https://github.com/tmlmt/milk-tracker/commit/d9e1fce9f6de013473d776d4da661732fbb2ba4f)) - Thomas Lamant
- **(tables)** improve sticky cells color - ([c8cc4c0](https://github.com/tmlmt/milk-tracker/commit/c8cc4c096d3be01010b4cb8351f8e09e291ae425)) - Thomas Lamant

### 🏡 Chore

- **(app)** remove print statements - ([419de0a](https://github.com/tmlmt/milk-tracker/commit/419de0aa4b3c7e8eae82a5dc44cc906f768cffaa)) - Thomas Lamant
- **(coverage)** update badge - ([46eed25](https://github.com/tmlmt/milk-tracker/commit/46eed252782298b9836b339a7990327e607d439e)) - github-actions[bot]
- **(main)** remove unused variables - ([6b9d08e](https://github.com/tmlmt/milk-tracker/commit/6b9d08e9ae52b0a0699db5b499b8a6587b69bfae)) - Thomas Lamant

---
## [2.0.0-beta.2](https://github.com/tmlmt/milk-tracker/compare/v2.0.0-beta.1..v2.0.0-beta.2) - 2024-06-07

### 🤖 CI

- add coverage badge - ([f383faa](https://github.com/tmlmt/milk-tracker/commit/f383faaba16670b2b9cd0bcb2d86c2c61e15f8ec)) - Thomas Lamant

### 🏡 Chore

- **(coverage)** update badge - ([a669b20](https://github.com/tmlmt/milk-tracker/commit/a669b203efca3321fcdfa982d13a5a21bd1d2f8f)) - github-actions[bot]
- **(readme)** add text, version and coverage badges - ([68fd19e](https://github.com/tmlmt/milk-tracker/commit/68fd19eb4a1f185ec93b1a3353dba2f096cbf5e7)) - Thomas Lamant

---
## [2.0.0-beta.1](https://github.com/tmlmt/milk-tracker/compare/v2.0.0-beta.0..v2.0.0-beta.1) - 2024-06-07

### 🚀 Enhancements

- **(stats)** add time since previous end - ([c3d6c78](https://github.com/tmlmt/milk-tracker/commit/c3d6c78a0fa2c3dab138c84cf00791346b32241c)) - Thomas Lamant
- responsive tables - ([92c981c](https://github.com/tmlmt/milk-tracker/commit/92c981cfc28fa144f4d4154f44ce436d218818de)) - Thomas Lamant

### 🚜 Refactor

- resolve PD011 - ([faa79b1](https://github.com/tmlmt/milk-tracker/commit/faa79b14198dd7d45e1faa1a024ce973ffecc578)) - Thomas Lamant
- move title, port and max_password_attempts to config and env files - ([1a234b7](https://github.com/tmlmt/milk-tracker/commit/1a234b71ea3614f80ca0116e197945b287cf6942)) - Thomas Lamant

### 🏡 Chore

- **(env)** add sass - ([4048e08](https://github.com/tmlmt/milk-tracker/commit/4048e086c844f84ac33317e68cc926850fdf8818)) - Thomas Lamant
- **(main)** remove unused imports - ([dbfef3f](https://github.com/tmlmt/milk-tracker/commit/dbfef3f26a07b703abd812cd0a53e4645b09ed4f)) - Thomas Lamant
- remove unused SSL capability - ([d742009](https://github.com/tmlmt/milk-tracker/commit/d7420093208e82b64b394ba3220ab23732ff88bf)) - Thomas Lamant
- add TODO - ([0f3f457](https://github.com/tmlmt/milk-tracker/commit/0f3f4571252a1829b379499f362f41b78cda87ea)) - Thomas Lamant

---
## [2.0.0-beta.0](https://github.com/tmlmt/milk-tracker/compare/v1.3.0..v2.0.0-beta.0) - 2024-06-06

### 🚀 Enhancements

- **(summary_table)** reverse order - ([38e6f5d](https://github.com/tmlmt/milk-tracker/commit/38e6f5daec79bcbc7b0c2a1eb841a994bc9816c8)) - Thomas Lamant
- order latest table meal backwards - ([5260263](https://github.com/tmlmt/milk-tracker/commit/526026366eef22686811db5206f6cfcbc10454a6)) - Thomas Lamant

### 🚜 Refactor

- introduce model and controller design pattern - ([3b5688c](https://github.com/tmlmt/milk-tracker/commit/3b5688c6fc36c5702de04bc33d70e8e351cd9bb9)) - Thomas Lamant
- introduce data models for ongoing and finished meals - ([eb61515](https://github.com/tmlmt/milk-tracker/commit/eb61515bc5a2c301ac0d8d6b6f7b83f41a515d80)) - Thomas Lamant

### 🎨 Style

- format imports and auto-format imports on save - ([5f17a9d](https://github.com/tmlmt/milk-tracker/commit/5f17a9de074516d7490b22aa9a5d9f1f420865a2)) - Thomas Lamant
- apply stricter linting rules - ([4377c1d](https://github.com/tmlmt/milk-tracker/commit/4377c1d41b8383e8bfcb8a0d0ab58c635e01ce25)) - Thomas Lamant
- reorganize libs and lint - ([8a15b65](https://github.com/tmlmt/milk-tracker/commit/8a15b65ebcdec3bab7022745ca488b258e4642fd)) - Thomas Lamant

### 🌊 Types

- **(main)** fix imports and other misc errors - ([a4a8a27](https://github.com/tmlmt/milk-tracker/commit/a4a8a276697fe6fd29c57bbfdd5126668eec2b6e)) - Thomas Lamant
- fix is_time_format() - ([cadec8c](https://github.com/tmlmt/milk-tracker/commit/cadec8cb9569d594305131da181bf81642398d61)) - Thomas Lamant

### 🧪 Tests

- add tests for meal schemas and time utils - ([6852ca5](https://github.com/tmlmt/milk-tracker/commit/6852ca5a981ea57610dc6ed53114437084230c5a)) - Thomas Lamant

### 🏡 Chore

- **(dev)** rename vscode workspace - ([65efa09](https://github.com/tmlmt/milk-tracker/commit/65efa0967558db426940b7203952b0553aab626c)) - Thomas Lamant
- **(mypy)** activate pydantic plugin - ([c39c0dc](https://github.com/tmlmt/milk-tracker/commit/c39c0dc4303e183623a8e87f79e8121b8f007c39)) - Thomas Lamant
- avoid using mypy daemon as it prevents mypy from being called - ([3e80296](https://github.com/tmlmt/milk-tracker/commit/3e80296184344ba6e559ff97afa7420e1f189617)) - Thomas Lamant
- designate milk_tracker as package - ([06f0010](https://github.com/tmlmt/milk-tracker/commit/06f001058c6f437aef4b7d5c93bf5b3d900f712e)) - Thomas Lamant
- update env file - ([0be6e36](https://github.com/tmlmt/milk-tracker/commit/0be6e3633480a6faccf0d3f37bc4b15374bf4762)) - Thomas Lamant

---
## [1.3.0](https://github.com/tmlmt/milk-tracker/compare/v1.2.0..v1.3.0) - 2024-06-01

### 🚀 Enhancements

- improve charts interaction and display on mobile - ([a4f10e6](https://github.com/tmlmt/milk-tracker/commit/a4f10e63a00720bdf14e0b8bc1d104fd91f37243)) - Thomas Lamant

### 🩹 Fixes

- column names in last meals table - ([1eaea92](https://github.com/tmlmt/milk-tracker/commit/1eaea92d13b9470e144ed84ad02f30851cb67968)) - Thomas Lamant
- some display improvements on mobile - ([75e9bca](https://github.com/tmlmt/milk-tracker/commit/75e9bca2e6883d37eadbb10006b704a85b1f8074)) - Thomas Lamant

### 🏡 Chore

- format main.py - ([31901c1](https://github.com/tmlmt/milk-tracker/commit/31901c19441ed63d7e31ce869fd82b1d51ecb604)) - Thomas Lamant

---
## [1.2.0](https://github.com/tmlmt/milk-tracker/compare/v1.1.0..v1.2.0) - 2024-05-30

### 🚀 Enhancements

- **(new_meal)** lock start time - ([a9077ce](https://github.com/tmlmt/milk-tracker/commit/a9077cec861fce9e44c49331d8f196f191ab7061)) - Thomas Lamant
- delete latest meal - ([a96ebdd](https://github.com/tmlmt/milk-tracker/commit/a96ebdd73077bbe8e144e6fcab62668a1a7d22a4)) - Thomas Lamant

### 🤖 CI

- deploy workflow (#7) - ([eacb7aa](https://github.com/tmlmt/milk-tracker/commit/eacb7aa82ee9aa4a366335bf794cc82daabfdcf1)) - Thomas Lamant

### 🏡 Chore

- **(changelog)** fix repo url - ([592d7b3](https://github.com/tmlmt/milk-tracker/commit/592d7b396493082c9bef8b4bd2711967c68cacdd)) - Thomas Lamant
- **(changelog)** v1.2 - ([6f79dea](https://github.com/tmlmt/milk-tracker/commit/6f79deaef063177a39eb109a9e76a5cab6e635a4)) - Thomas Lamant
- ignore journal files and replace file in repo with template - ([de96af5](https://github.com/tmlmt/milk-tracker/commit/de96af5360a1f322291758962e42e1391a12f487)) - Thomas Lamant

---
## [1.1.0](https://github.com/tmlmt/milk-tracker/compare/v1.0.0..v1.1.0) - 2024-05-28

### 🚀 Enhancements

- **(charts)** show duration in minutes instead of hours - ([5d3cdad](https://github.com/tmlmt/milk-tracker/commit/5d3cdadbd20be0f73341551c57879f07d7eff5db)) - Thomas Lamant
- **(charts)** set yaxis to start at 0 - ([3e3f3e6](https://github.com/tmlmt/milk-tracker/commit/3e3f3e6b731f25fe4690b347a4fffe19e917b276)) - Thomas Lamant
- **(new_meal)** input field masks and validation - ([a350f01](https://github.com/tmlmt/milk-tracker/commit/a350f01ec4a3002e133e89a71ccfcebc73e452b3)) - Thomas Lamant

### 🩹 Fixes

- **(force_update)** also update every-minute continuous update fields - ([727e628](https://github.com/tmlmt/milk-tracker/commit/727e6288fc947d8b447f9ff7ce9978f15606851e)) - Thomas Lamant
- **(new_meal)** lazy-rules and unwanted menu opening on click - ([ebbe66a](https://github.com/tmlmt/milk-tracker/commit/ebbe66a73cc8dd95538ac4452106f86c3b53d3c4)) - Thomas Lamant

### 🔥 Performance

- no need to dedent markdown multi-lines - ([171169b](https://github.com/tmlmt/milk-tracker/commit/171169bf4051f495eeb294854211e78fb812b5b4)) - Thomas Lamant

### 🎨 Style

- **(new_meal)** smaller input fields - ([166c958](https://github.com/tmlmt/milk-tracker/commit/166c958d806e0ca8b24c6b25565b9fe463c42db9)) - Thomas Lamant
- display latest_meal_info as a text block instead of a list - ([0af0d16](https://github.com/tmlmt/milk-tracker/commit/0af0d16568df2839e52c4a1c4d1f0dabaa72047e)) - Thomas Lamant

### 🏡 Chore

- **(changelog)** v1.1.0 - ([92dc1ec](https://github.com/tmlmt/milk-tracker/commit/92dc1ecbe430ff3015c83ba5df0d35752c4532b3)) - Thomas Lamant
- add config file for git-cliff - ([fa98f3f](https://github.com/tmlmt/milk-tracker/commit/fa98f3f0b222053de714fbdc6d35a863c6fe27f0)) - Thomas Lamant

---
## [1.0.0] - 2024-05-28

### Highlights

Minimum Viable Product

### 🚀 Enhancements

- mvp - ([b9bab5e](https://github.com/tmlmt/milk-tracker/commit/b9bab5e7553b19ffc61be9dbcbb07045d93e754c)) - Thomas Lamant
- enable running with ssl - ([52ab3e5](https://github.com/tmlmt/milk-tracker/commit/52ab3e542a23d65ca35dd2cd31ad2dff645872b7)) - Thomas Lamant
- add SSL_ENABLED toggle env var - ([c5e8e98](https://github.com/tmlmt/milk-tracker/commit/c5e8e98292a98f3e3900a592a28598b29ff11389)) - Thomas Lamant
- password authorization - ([bb56652](https://github.com/tmlmt/milk-tracker/commit/bb566526543a0ec0217392de53a81a93ec0a7c28)) - Thomas Lamant

### 🩹 Fixes

- restore journal file to default - ([e0d376f](https://github.com/tmlmt/milk-tracker/commit/e0d376f3a463145afec069b30c6df09bbafdb70e)) - Thomas Lamant

### 🎨 Style

- add page title - ([b950e22](https://github.com/tmlmt/milk-tracker/commit/b950e2226c56f66b875ed6aa91fa49531c2c353a)) - Thomas Lamant

### 🏡 Chore

- export micromamba/conda env spec file - ([1456483](https://github.com/tmlmt/milk-tracker/commit/14564833ee12201bcbea095a5ad03307d8f06da3)) - Thomas Lamant
- assign port and disable auto-show - ([73e7ba7](https://github.com/tmlmt/milk-tracker/commit/73e7ba71bab8a91c4b2eccfe00ca5b2eb2513b5d)) - Thomas Lamant
- ignore .nicegui folder - ([420e9ee](https://github.com/tmlmt/milk-tracker/commit/420e9ee7ca87fa4636abdaa2c551fbb56d9a3ceb)) - Thomas Lamant
- update env specs with argon2 - ([dee8030](https://github.com/tmlmt/milk-tracker/commit/dee8030ade77d7efbd8240423a8cd6310f5b2578)) - Thomas Lamant

<!-- generated by git-cliff -->
