import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewConsutationComponent } from './new-consutation.component';

describe('NewConsutationComponent', () => {
  let component: NewConsutationComponent;
  let fixture: ComponentFixture<NewConsutationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewConsutationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewConsutationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
