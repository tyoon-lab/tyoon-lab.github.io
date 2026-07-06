# Yoon Lab 홈페이지 초안 — Ruby 4 / 최신 Jekyll용

이 버전은 **Ruby 4.x 또는 최신 Ruby 환경에서 로컬 미리보기**가 되도록 `github-pages` gem 대신 최신 Jekyll 4.x 계열을 사용합니다.

## 1. 로컬 미리보기

압축을 푼 뒤 `yoonlab-homepage` 폴더 안에서 명령 프롬프트를 열고 아래를 실행하세요.

```cmd
ruby -v
gem -v
gem install bundler
bundle install
bundle exec jekyll serve --livereload
```

성공하면 브라우저에서 아래 주소로 접속합니다.

```text
http://localhost:4000
```

명령 프롬프트에 아래와 비슷하게 나오면 정상입니다.

```text
Server address: http://127.0.0.1:4000/
Server running... press ctrl-c to stop.
```

## 2. 기존 `Gemfile.lock` 문제

예전에 Ruby 4.0, Ruby 3.1 등 다른 버전에서 실행하다가 문제가 났다면, 폴더 안에서 아래 파일을 삭제한 뒤 다시 실행하세요.

```cmd
del Gemfile.lock
bundle install
bundle exec jekyll serve --livereload
```

이 압축본에는 처음부터 `Gemfile.lock`을 넣지 않았습니다.

## 3. 주로 수정할 파일

논문, 뉴스, 멤버 정보는 아래 YAML 파일만 수정하면 됩니다.

```text
_data/publications.yml
_data/highlights.yml
_data/members.yml
_data/news.yml
_data/research.yml
```

페이지 본문은 아래 파일을 수정합니다.

```text
index.html
research.md
people.md
publications.md
news.md
join.md
contact.md
```

## 4. GitHub Pages 배포 메모

이 버전은 최신 Jekyll 기반입니다. GitHub Pages에서 GitHub의 기본 Jekyll 빌드를 그대로 쓰기보다, 나중에는 GitHub Actions로 빌드/배포하는 방식을 권장합니다. 그래야 로컬에서 쓰는 최신 Jekyll 환경과 GitHub 배포 환경이 맞습니다.

## 5. 디자인 방향

- Main color: deep navy / charcoal
- Accent color: muted gold
- Identity message: Decoding Electrochemical Interfaces, Degradation, and Corrosion
- Core sections: Research Themes, Featured Research Highlights, News & Opportunities, Join Us
