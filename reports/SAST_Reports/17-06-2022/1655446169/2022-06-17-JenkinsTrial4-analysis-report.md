# Code analysis
## JenkinsTrial4 
#### Version 1.0 

**By: default**

*Date: 2022-06-17*

## Introduction
This document contains results of the code analysis of JenkinsTrial4



## Configuration

- Quality Profiles
    - Names: Sonar way [PHP]; Sonar way [Python]; 
    - Files: AYBqrPLIN0_tCdZCZ0yT.json; AYBqrO2WN0_tCdZCZ0EW.json; 


 - Quality Gate
    - Name: Sonar way
    - File: Sonar way.xml

## Synthesis

### Analysis Status

Reliability | Security | Security Review | Maintainability |
:---:|:---:|:---:|:---:
B | A | E | A |

### Quality gate status

| Quality Gate Status | OK |
|-|-|

Metric|Value
---|---
Reliability Rating on New Code|OK
Security Rating on New Code|OK
Maintainability Rating on New Code|OK
Coverage on New Code|OK
Duplicated Lines (%) on New Code|OK


### Metrics

Coverage | Duplications | Comment density | Median number of lines of code per file | Adherence to coding standard |
:---:|:---:|:---:|:---:|:---:
0.0 % | 17.3 % | 9.1 % | 12.0 | 99.6 %

### Tests

Total | Success Rate | Skipped | Errors | Failures |
:---:|:---:|:---:|:---:|:---:
0 | 0 % | 0 | 0 | 0

### Detailed technical debt

Reliability|Security|Maintainability|Total
---|---|---|---
0d 0h 5min|-|0d 1h 0min|0d 1h 5min


### Metrics Range

\ | Cyclomatic Complexity | Cognitive Complexity | Lines of code per file | Coverage | Comment density (%) | Duplication (%)
:---|:---:|:---:|:---:|:---:|:---:|:---:
Min | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0
Max | 57.0 | 134.0 | 270.0 | 0.0 | 12.5 | 40.0

### Volume

Language|Number
---|---
PHP|252
Python|18
Total|270


## Issues

### Issues count by severity and types

Type / Severity|INFO|MINOR|MAJOR|CRITICAL|BLOCKER
---|---|---|---|---|---
BUG|0|1|0|0|0
VULNERABILITY|0|0|0|0|0
CODE_SMELL|0|1|5|2|0


### Issues List

Name|Description|Type|Severity|Number
---|---|---|---|---
Image, area and button with image tags should have an "alt" attribute|The alt attribute provides a textual alternative to an image. <br /> It is used whenever the actual image cannot be rendered. <br /> Common reasons for that include: <br />  <br />    The image can no longer be found  <br />    Visually impaired users using a screen reader software  <br />    Images loading is disabled, to reduce data consumption on mobile phones  <br />  <br /> It is also very important to not set an alt attribute to a non-informative value. For example &lt;img ... alt="logo"&gt; <br /> is useless as it doesn't give any information to the user. In this case, as for any other decorative image, it is better to use a CSS background image <br /> instead of an &lt;img&gt; tag. If using CSS background-image is not possible, an empty alt="" is tolerated. See Exceptions <br /> bellow. <br /> This rule raises an issue when <br />  <br />    an &lt;input type="image"&gt; tag or an &lt;area&gt; tag have no alt attribute or their <br />   alt&nbsp;attribute has an empty string value.  <br />    an &lt;img&gt; tag has no alt attribute.  <br />  <br /> Noncompliant Code Example <br />  <br /> &lt;img src="foo.png" /&gt; &lt;!-- Noncompliant --&gt; <br /> &lt;input type="image" src="bar.png" /&gt; &lt;!-- Noncompliant --&gt; <br /> &lt;input type="image" src="bar.png" alt="" /&gt; &lt;!-- Noncompliant --&gt; <br />  <br /> &lt;img src="house.gif" usemap="#map1" <br />     alt="rooms of the house." /&gt; <br /> &lt;map id="map1" name="map1"&gt; <br />   &lt;area shape="rect" coords="0,0,42,42" <br />     href="bedroom.html"/&gt; &lt;!-- Noncompliant --&gt; <br />   &lt;area shape="rect" coords="0,0,21,21" <br />     href="lounge.html" alt=""/&gt; &lt;!-- Noncompliant --&gt; <br /> &lt;/map&gt; <br />  <br /> Compliant Solution <br />  <br /> &lt;img src="foo.png" alt="Some textual description of foo.png" /&gt; <br /> &lt;input type="image" src="bar.png" alt="Textual description of bar.png" /&gt; <br />  <br /> &lt;img src="house.gif" usemap="#map1" <br />     alt="rooms of the house." /&gt; <br /> &lt;map id="map1" name="map1"&gt; <br />   &lt;area shape="rect" coords="0,0,42,42" <br />     href="bedroom.html" alt="Bedroom" /&gt; <br />   &lt;area shape="rect" coords="0,0,21,21" <br />     href="lounge.html" alt="Lounge"/&gt; <br /> &lt;/map&gt; <br />  <br /> Exceptions <br /> &lt;img&gt; tags with empty string&nbsp;alt="" attributes won't raise any issue. However this technic should be used in <br /> two cases only: <br /> When the image is decorative and it is not possible to use a CSS background image. For example, when the decorative &lt;img&gt; is <br /> generated via javascript with a source image coming from a database, it is better to use an &lt;img alt=""&gt; tag rather than generate <br /> CSS code. <br />  <br /> &lt;li *ngFor="let image of images"&gt; <br />     &lt;img [src]="image" alt=""&gt; <br /> &lt;/li&gt; <br />  <br /> When the image is not decorative but it's alt text would repeat a nearby text. For example, images contained in links should not <br /> duplicate the link's text in their alt attribute, as it would make the screen reader repeat the text twice. <br />  <br /> &lt;a href="flowers.html"&gt; <br />     &lt;img src="tulip.gif" alt="" /&gt; <br />     A blooming tulip <br /> &lt;/a&gt; <br />  <br /> In all other cases you should use CSS background images. <br /> See&nbsp;W3C WAI&nbsp;Web Accessibility Tutorials&nbsp;for more <br /> information. <br /> See <br />  <br />    WCAG2, H24 - Providing text alternatives for the area elements of image maps  <br />    WCAG2, H36 - Using alt attributes on images used as submit buttons  <br />    WCAG2, H37 - Using alt attributes on img elements  <br />    WCAG2, H67 - Using null alt text and no title attribute on img elements for images <br />   that AT should ignore  <br />    WCAG2, H2 - Combining adjacent image and text links for the same resource  <br />    WCAG2, 1.1.1 - Non-text Content  <br />    WCAG2, 2.4.4 - Link Purpose (In Context)  <br />    WCAG2, 2.4.9 - Link Purpose (Link Only)  <br /> |BUG|MINOR|1
Control structures should use curly braces|While not technically incorrect, the omission of curly braces can be misleading, and may lead to the introduction of errors during maintenance. <br /> Noncompliant Code Example <br />  <br /> if (condition)  // Noncompliant <br />   executeSomething(); <br />  <br /> Compliant Solution <br />  <br /> if (condition) { <br />   executeSomething(); <br /> } <br />  <br /> See <br />  <br />    CERT, EXP19-C. - Use braces for the body of an if, for, or while statement  <br />    CERT, EXP52-J. - Use braces for the body of an if, for, or while statement  <br /> |CODE_SMELL|CRITICAL|2
Source files should not have any duplicated blocks|An issue is created on a file as soon as there is at least one block of duplicated code on this file|CODE_SMELL|MAJOR|2
Collapsible "if" statements should be merged|Merging collapsible if statements increases the code's readability. <br /> Noncompliant Code Example <br />  <br /> if (condition1) { <br />   if (condition2) { <br />     ... <br />   } <br /> } <br />  <br /> Compliant Solution <br />  <br /> if (condition1 &amp;&amp; condition2) { <br />   ... <br /> } <br /> |CODE_SMELL|MAJOR|2
Sections of code should not be commented out|Programmers should not comment out code as it bloats programs and reduces readability. <br /> Unused code should be deleted and can be retrieved from source control history if required.|CODE_SMELL|MAJOR|1
A close curly brace should be located at the beginning of a line|Shared coding conventions make it possible for a team to efficiently collaborate. This rule makes it mandatory to place a close curly brace at the <br /> beginning of a line. <br /> Noncompliant Code Example <br />  <br /> if(condition) { <br />   doSomething();} <br />  <br /> Compliant Solution <br />  <br /> if(condition) { <br />   doSomething(); <br /> } <br />  <br /> Exceptions <br /> When blocks are inlined (open and close curly braces on the same line), no issue is triggered.  <br />  <br /> if(condition) {doSomething();} <br /> |CODE_SMELL|MINOR|1


## Security Hotspots

### Security hotspots count by category and priority

Category / Priority|LOW|MEDIUM|HIGH
---|---|---|---
LDAP Injection|0|0|0
Object Injection|0|0|0
Server-Side Request Forgery (SSRF)|0|0|0
XML External Entity (XXE)|0|0|0
Insecure Configuration|0|0|0
XPath Injection|0|0|0
Authentication|0|0|1
Weak Cryptography|0|0|0
Denial of Service (DoS)|0|0|0
Log Injection|0|0|0
Cross-Site Request Forgery (CSRF)|0|0|0
Open Redirect|0|0|0
SQL Injection|0|0|0
Buffer Overflow|0|0|0
File Manipulation|0|0|0
Code Injection (RCE)|0|0|0
Cross-Site Scripting (XSS)|0|0|0
Command Injection|0|0|0
Path Traversal Injection|0|0|0
HTTP Response Splitting|0|0|0
Others|0|0|0


### Security hotspots

Category|Name|Priority|Severity|Count
---|---|---|---|---
Authentication|Hard-coded credentials are security-sensitive|HIGH|BLOCKER|1
