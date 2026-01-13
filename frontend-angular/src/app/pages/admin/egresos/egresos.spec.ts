import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Egresos } from './egresos';

describe('Egresos', () => {
  let component: Egresos;
  let fixture: ComponentFixture<Egresos>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Egresos]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Egresos);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
